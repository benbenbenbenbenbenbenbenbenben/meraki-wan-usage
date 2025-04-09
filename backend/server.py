from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import meraki
from datetime import datetime, timedelta
from collections import defaultdict
import os
import time

app = Flask(__name__, static_folder="dist", static_url_path="")

# Enable CORS only in development
if os.environ.get("FLASK_ENV") == "development":
    CORS(app)

try:
    dashboard = meraki.DashboardAPI(suppress_logging=True)
except meraki.exceptions.APIKeyError:
    dashboard = None
    print("⚠️  MERAKI_DASHBOARD_API_KEY is missing or invalid.")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/api/status', methods=['GET'])
def check_meraki_key_status():
    api_key = os.environ.get("MERAKI_DASHBOARD_API_KEY")

    if not api_key or api_key.strip() == "":
        return jsonify({
            "status": "error",
            "title": "API Key Missing",
            "message": "Your Meraki Dashboard API key is not set. Please add MERAKI_DASHBOARD_API_KEY to your environment variables.",
            "code": "NO_API_KEY"
        }), 400

    try:
        test_dashboard = meraki.DashboardAPI(api_key, suppress_logging=True)
        orgs = test_dashboard.organizations.getOrganizations()
        return jsonify({"status": "ok", "organizations": orgs})
    except Exception as e:
        return jsonify({
            "status": "error",
            "title": "Invalid API Key",
            "message": "The provided Meraki API key is invalid or doesn't have access to any organizations.",
            "code": "INVALID_API_KEY",
            "details": str(e)
        }), 403


@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    try:
        orgs = dashboard.organizations.getOrganizations()
        return jsonify(orgs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def chunk_date_range(start, end, max_days=7):
    intervals = []
    while start < end:
        chunk_end = min(start + timedelta(days=max_days), end)
        intervals.append((start, chunk_end))
        start = chunk_end
    return intervals


@app.route('/api/meraki/uplinks/<org_id>', methods=['GET'])
def get_organization_uplink_usage(org_id):
    import time
    start_time = time.time()

    mode = request.args.get("mode", "single-day")
    ranges = []

    if mode == "single-day":
        date_str = request.args.get("date")
        if not date_str:
            return jsonify({"error": "Missing 'date'"}), 400
        start = datetime.fromisoformat(date_str).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        ranges = [(start, end)]

    elif mode in ("month", "week"):
        start_str = request.args.get("start")
        end_str = request.args.get("end")
        if not start_str or not end_str:
            return jsonify({"error": "Missing start/end"}), 400
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        ranges = chunk_date_range(start, end) if mode == "month" else [(start, end)]

    elif mode == "compare-days":
        dates = request.args.get("dates", "").split(",")
        if len(dates) != 2:
            return jsonify({"error": "Need two dates for compare-days"}), 400
        for d in dates:
            start = datetime.fromisoformat(d).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            ranges.append((start, end))

    elif mode == "compare-weeks":
        week_ranges = request.args.get("weeks", "").split(",")
        if len(week_ranges) != 4:
            return jsonify({"error": "Need 2 weeks (start,end,start,end)"}), 400
        for i in range(0, 4, 2):
            start = datetime.fromisoformat(week_ranges[i])
            end = datetime.fromisoformat(week_ranges[i + 1])
            ranges.append((start, end))

    else:
        return jsonify({"error": "Unsupported mode"}), 400

    if mode.startswith("compare-"):
        half = len(ranges) // 2
        dataset1 = fetch_aggregated_uplink_data(ranges[:half], org_id)
        dataset2 = fetch_aggregated_uplink_data(ranges[half:], org_id)
        return jsonify({"primary": dataset1, "compare": dataset2})

    dataset = fetch_aggregated_uplink_data(ranges, org_id)
    return jsonify(dataset)


def fetch_aggregated_uplink_data(ranges, org_id):
    def init_uplink(serial, iface):
        return {"serial": serial, "interface": iface, "sent": 0, "received": 0}

    usage_map = {}
    networks = dashboard.organizations.getOrganizationNetworks(org_id)

    network_lookup = {
        net["id"]: {
            "name": net["name"],
            "tags": net.get("tags", []),
        }
        for net in networks
    }

    for start, end in ranges:
        usage = dashboard.appliance.getOrganizationApplianceUplinksUsageByNetwork(
            organizationId=org_id,
            t0=start.isoformat(),
            t1=end.isoformat(),
        )

        for network in usage:
            net_id = network.get("networkId")
            net_info = network_lookup.get(net_id, {})
            net_tags = net_info.get("tags", [])
            net_name = network.get("name")
            key = net_id

            if key not in usage_map:
                usage_map[key] = {
                    "networkId": net_id,
                    "name": net_name,
                    "tags": net_tags,
                    "byUplink": []
                }

            uplink_index_map = {
                (u["serial"], u["interface"]): u
                for u in usage_map[key]["byUplink"]
            }

            for uplink in network.get("byUplink", []):
                serial = uplink.get("serial")
                iface = uplink.get("interface")
                k = (serial, iface)

                if k not in uplink_index_map:
                    new_uplink = init_uplink(serial, iface)
                    usage_map[key]["byUplink"].append(new_uplink)
                    uplink_index_map[k] = new_uplink

                uplink_index_map[k]["sent"] += uplink.get("sent", 0)
                uplink_index_map[k]["received"] += uplink.get("received", 0)

    return list(usage_map.values())


if __name__ == '__main__':
    port = int(os.environ.get("FLASK_PORT", 5005))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, port=port, host="0.0.0.0")
