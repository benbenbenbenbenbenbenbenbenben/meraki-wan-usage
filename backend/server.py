from flask import Flask, request, jsonify
from flask_cors import CORS
import meraki
from datetime import datetime, timedelta
from collections import defaultdict
import os
import time

app = Flask(__name__)
CORS(app)

dashboard = meraki.DashboardAPI(suppress_logging=True)

test_data = [{'networkId': 'N_622622648484016986', 'name': 'ISP Router', 'byUplink': [{'serial': 'Q2YN-28GQ-UALD', 'interface': 'wan1', 'sent': 2470127273, 'received': 1587011603}]}, {'networkId': 'N_622622648484016987', 'name': 'Data Center 2', 'byUplink': [{'serial': 'Q2YN-RJNQ-HT8L', 'interface': 'wan1', 'sent': 762467559, 'received': 776154357}]}, {'networkId': 'N_622622648484016988', 'name': 'Data Center 1', 'byUplink': [{'serial': 'Q2YN-FECM-KNGK', 'interface': 'wan1', 'sent': 763556516, 'received': 775917350}]}, {'networkId': 'L_622622648484039080', 'name': 'Lab 1', 'byUplink': [{'serial': 'Q2YN-XLRM-LZG2', 'interface': 'wan1', 'sent': 143122208, 'received': 158767899}, {'serial': 'Q2YN-XLRM-LZG2', 'interface': 'wan2', 'sent': 18162243, 'received': 96845452}]}, {'networkId': 'L_622622648484039081', 'name': 'Lab 2', 'byUplink': [{'serial': 'Q2YN-WT44-4ZYB', 'interface': 'wan1', 'sent': 766092829, 'received': 719638570}, {'serial': 'Q2YN-WT44-4ZYB', 'interface': 'wan2', 'sent': 623425579, 'received': 644713620}]}, {'networkId': 'L_622622648484039082', 'name': 'Lab 3', 'byUplink': [{'serial': 'Q2YN-BDD9-52QY', 'interface': 'wan1', 'sent': 149574352, 'received': 158602003}, {'serial': 'Q2YN-BDD9-52QY', 'interface': 'wan2', 'sent': 18156462, 'received': 96818075}]}, {'networkId': 'L_622622648484039083', 'name': 'Lab 4', 'byUplink': [{'serial': 'Q2YN-WWN5-QP94', 'interface': 'wan1', 'sent': 153623937, 'received': 158533534}, {'serial': 'Q2YN-WWN5-QP94', 'interface': 'wan2', 'sent': 18161309, 'received': 96707134}]}, {'networkId': 'L_622622648484039084', 'name': 'Lab 5', 'byUplink': [{'serial': 'Q2YN-DHN7-R8CF', 'interface': 'wan1', 'sent': 150601577, 'received': 158707683}, {'serial': 'Q2YN-DHN7-R8CF', 'interface': 'wan2', 'sent': 18159238, 'received': 96731047}]}, {'networkId': 'L_622622648484039085', 'name': 'Lab 6', 'byUplink': [{'serial': 'Q2YN-EG7H-KKLB', 'interface': 'wan1', 'sent': 150014322, 'received': 157955566}, {'serial': 'Q2YN-EG7H-KKLB', 'interface': 'wan2', 'sent': 18162495, 'received': 96595764}]}, {'networkId': 'L_622622648484039086', 'name': 'Lab 7', 'byUplink': [{'serial': 'Q2YN-QUHU-RT3U', 'interface': 'wan1', 'sent': 766150546, 'received': 713748372}, {'serial': 'Q2YN-QUHU-RT3U', 'interface': 'wan2', 'sent': 623180292, 'received': 578359470}]}, {'networkId': 'L_622622648484039087', 'name': 'Lab 8', 'byUplink': [{'serial': 'Q2YN-ND6S-686V', 'interface': 'wan1', 'sent': 151876658, 'received': 158671907}, {'serial': 'Q2YN-ND6S-686V', 'interface': 'wan2', 'sent': 18163408, 'received': 28676439}]}, {'networkId': 'L_622622648484039088', 'name': 'Lab 9', 'byUplink': [{'serial': 'Q2YN-4T95-GP3L', 'interface': 'wan1', 'sent': 161438702, 'received': 165694094}, {'serial': 'Q2YN-4T95-GP3L', 'interface': 'wan2', 'sent': 18119299, 'received': 28801256}]}, {'networkId': 'L_622622648484039089', 'name': 'Lab 10', 'byUplink': [{'serial': 'Q2YN-PBVC-5RBP', 'interface': 'wan1', 'sent': 62458143, 'received': 124160458}, {'serial': 'Q2YN-PBVC-5RBP', 'interface': 'wan2', 'sent': 18169124, 'received': 28748492}]}, {'networkId': 'L_622622648484039091', 'name': 'Lab 12', 'byUplink': [{'serial': 'Q2PN-3QFM-QXAY', 'interface': 'cellular', 'sent': 0, 'received': 0}, {'serial': 'Q2PN-3QFM-QXAY', 'interface': 'wan1', 'sent': 475630418, 'received': 577289468}, {'serial': 'Q2PN-3QFM-QXAY', 'interface': 'wan2', 'sent': 359376896, 'received': 461317363}]}, {'networkId': 'L_622622648484039092', 'name': 'Lab 13', 'byUplink': [{'serial': 'Q2PN-MA3L-9LMB', 'interface': 'cellular', 'sent': 0, 'received': 0}, {'serial': 'Q2PN-MA3L-9LMB', 'interface': 'wan1', 'sent': 127914307, 'received': 128262833}, {'serial': 'Q2PN-MA3L-9LMB', 'interface': 'wan2', 'sent': 9503880, 'received': 18291954}]}, {'networkId': 'L_622622648484039093', 'name': 'Lab 14', 'byUplink': [{'serial': 'Q2PN-X37X-95VC', 'interface': 'wan1', 'sent': 38668313, 'received': 92142924}, {'serial': 'Q2PN-X37X-95VC', 'interface': 'wan2', 'sent': 9507737, 'received': 18305032}]}, {'networkId': 'L_622622648484039094', 'name': 'Lab 15', 'byUplink': [{'serial': 'Q2PN-MK2W-9XTK', 'interface': 'wan1', 'sent': 394708968, 'received': 538540045}, {'serial': 'Q2PN-MK2W-9XTK', 'interface': 'wan2', 'sent': 359405680, 'received': 461098156}]}]

def get_timespan(period):
    now = datetime.utcnow()
    if period == "day":
        return (now - timedelta(days=1)).isoformat()
    elif period == "week":
        return (now - timedelta(weeks=1)).isoformat()
    elif period == "month":
        return (now - timedelta(days=30)).isoformat()
    else:
        return (now - timedelta(days=1)).isoformat()

@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    try:
        orgs = dashboard.organizations.getOrganizations()
        return jsonify(orgs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/test_data', methods=['GET'])
def get_test_data():
    return jsonify(test_data)
    
# @app.route('/api/meraki/uplinks/<org_id>', methods=['GET'])
# def get_organization_uplink_usage(org_id):
#     try:
#         period = request.args.get("period", "day")
#         timespan = period_to_seconds(period)

#         # Step 1: Get network names
#         networks = dashboard.organizations.getOrganizationNetworks(org_id)
#         id_to_name = {net["id"]: net["name"] for net in networks}

#         # Step 2: Get uplink usage
#         usage = dashboard.appliance.getOrganizationApplianceUplinksUsageByNetwork(
#             organizationId=org_id,
#             timespan=timespan
#         )

#         # Step 3: Group results by network name
#         # results = {}
#         # for entry in usage:
#         #     net_id = entry.get("networkId")
#         #     name = id_to_name.get(net_id, net_id)
#         #     if name not in results:
#         #         results[name] = []
#         #     results[name].append(entry)

#         return jsonify(usage)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

def period_to_seconds(period):
    return {
        "day": 86400,
        "week": 604800,
        "month": 2592000
    }.get(period, 86400)



def chunk_date_range(start, end, max_days=7):
    """Splits a date range into subranges with max_days each."""
    intervals = []
    while start < end:
        print('chunk date')
        chunk_end = min(start + timedelta(days=max_days), end)
        print(chunk_end)
        intervals.append((start, chunk_end))
        start = chunk_end
        print(intervals)
    return intervals

@app.route('/api/meraki/uplinks/<org_id>', methods=['GET'])
def get_organization_uplink_usage(org_id):
  
        start_time = time.time()             
    # try:
        mode = request.args.get("mode", "single-day")

        if mode == "single-day":
            date_str = request.args.get("date")
            if not date_str:
                return jsonify({"error": "Missing 'date' for single-day mode"}), 400

            start = datetime.fromisoformat(date_str).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
            ranges = [(start, end)]

        elif mode == "billing-month":
            month_str = request.args.get("month")
            if not month_str:
                return jsonify({"error": "Missing 'month' for billing-month mode"}), 400

            year, month = map(int, month_str.split("-"))
            start = datetime(year, month, 1)
            end = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            ranges = chunk_date_range(start, end)

        elif mode == "compare-days":
            dates = request.args.get("dates", "").split(",")
            if len(dates) != 2:
                return jsonify({"error": "Need two dates for compare-days"}), 400

            ranges = []
            for d in dates:
                start = datetime.fromisoformat(d).replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(days=1)
                ranges.append((start, end))

        elif mode == "compare-months":
            months = request.args.get("months", "").split(",")
            if len(months) != 2:
                return jsonify({"error": "Need two months for compare-months"}), 400

            ranges = []
            for m in months:
                year, month = map(int, m.split("-"))
                start = datetime(year, month, 1)
                end = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
                ranges.extend(chunk_date_range(start, end))

        else:
            return jsonify({"error": "Unsupported mode"}), 400


        if mode.startswith("compare-"):
            dataset1 = fetch_aggregated_uplink_data(ranges[:len(ranges)//2], org_id )
            dataset2 = fetch_aggregated_uplink_data(ranges[len(ranges)//2:], org_id)
            elapsed = time.time() - start_time
            print(f"[uplinks route] org={org_id} took {elapsed:.2f}s")
            return jsonify({
                "primary": dataset1,
                "compare": dataset2
            })
        else:
            dataset = fetch_aggregated_uplink_data(ranges, org_id)
            elapsed = time.time() - start_time
            print(f"[uplinks route] org={org_id} took {elapsed:.2f}s")
            return jsonify(dataset)



    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


def fetch_aggregated_uplink_data(ranges, org_id):
    def init_uplink(serial, iface):
        return {"serial": serial, "interface": iface, "sent": 0, "received": 0}

    usage_map = {}

    networks = dashboard.organizations.getOrganizationNetworks(org_id)

    # Map with tags included
    network_lookup = {
        net["id"]: {
            "name": net["name"],
            "tags": net.get("tags", []),
        }
        for net in networks
    }

    for start, end in ranges:
        start_time = time.time() 
        print(f"Fetching uplinks from {start.isoformat()} to {end.isoformat()}")

        usage = dashboard.appliance.getOrganizationApplianceUplinksUsageByNetwork(
            organizationId=org_id,
            t0=start.isoformat(),
            t1=end.isoformat(),
        )
        
        elapsed = time.time() - start_time
        print(f"[getOrganizationApplianceUplinksUsageByNetwork] took {elapsed:.2f}s")

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
    app.run(debug=True)