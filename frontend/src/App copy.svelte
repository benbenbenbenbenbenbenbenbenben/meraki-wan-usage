<script lang="ts">
  import { onMount } from "svelte";

  type UplinkUsage = {
    networkId: string;
    networkName: string;
    interface: "wan1" | "wan2" | "cellular";
    serial: string;
    sent: number;
    received: number;
    total: number;
  };

  const uplinkData = $state<UplinkUsage[]>([]);

  let organizations = $state([]);
  let selectedOrg = $state("");
  let period = $state("day");
  let uplinkResults = $state([]);
  let loading = $state(false);
  let error = $state("");

  let interfaceFilter = $state("all");
  let sortBy = $state("total");
  let sortOrder = $state("desc");

  onMount(async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api/organizations");
      organizations = await res.json();
    } catch (e) {
      error = "Failed to load organizations.";
    }
  });

  async function getUplinkUsage(event) {
    event.preventDefault();
    if (!selectedOrg) return;

    uplinkResults = [];
    error = null;
    loading = true;

    try {
      const res = await fetch(
        // `http://127.0.0.1:5000/api/meraki/uplinks/${selectedOrg}?period=${period}`
        `http://127.0.0.1:5000/api/test_data`
      );

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Request failed");
      }

      const data = await res.json();
      console.log(data);
      const flat = [];

      for (const record of data) {
        const uplinks = record.byUplink || [];
        const networkName = record.name || "Unknown";

        for (const uplink of uplinks) {
          flat.push({
            network: networkName,
            interface: uplink.interface,
            sent: uplink.sent,
            received: uplink.received,
            total: uplink.sent + uplink.received,
            serial: uplink.serial,
          });
        }
      }

      console.log(flat);

      uplinkResults = flat;
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  const filtered = $derived(() => {
    const data = $uplinkResults;
    const iface = $interfaceFilter;
    const sort = $sortBy;
    const order = $sortOrder;

    return data
      .filter((r) => iface === "all" || r.interface === iface)
      .sort((a, b) => {
        const valA = a[sort];
        const valB = b[sort];
        return order === "asc" ? valA - valB : valB - valA;
      });
  });
</script>

<main class="container">
  <h1>Meraki Uplink Usage</h1>

  <form method="POST" onsubmit={getUplinkUsage}>
    <label>
      Organization
      <select bind:value={selectedOrg}>
        <option value="" disabled selected>Select an organization</option>
        {#each organizations as org}
          <option value={org.id}>{org.name}</option>
        {/each}
      </select>
    </label>

    <label>
      Time Period
      <select bind:value={period}>
        <option value="day">Last Day</option>
        <option value="week">Last Week</option>
        <option value="month">Last Month</option>
      </select>
    </label>

    <button type="submit" disabled={loading}>
      {loading ? "Loading..." : "Get Usage"}
    </button>
  </form>

  {#if error}
    <article class="contrast">
      <strong>Error:</strong>
      {error}
    </article>
  {/if}

  {#if uplinkResults.length > 0}
    <h2>Results</h2>

    <div class="filters">
      <label>
        Interface:
        <select bind:value={interfaceFilter}>
          <option value="all">All</option>
          <option value="wan1">WAN 1</option>
          <option value="wan2">WAN 2</option>
        </select>
      </label>

      <label>
        Sort By:
        <select bind:value={sortBy}>
          <option value="total">Total</option>
          <option value="sent">Sent</option>
          <option value="received">Received</option>
        </select>
      </label>

      <label>
        Order:
        <select bind:value={sortOrder}>
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </label>
    </div>

    <table>
      <thead>
        <tr>
          <th>Network</th>
          <th>Interface</th>
          <th>Serial</th>
          <th>Sent (MB)</th>
          <th>Received (MB)</th>
          <th>Total (MB)</th>
        </tr>
      </thead>
      <tbody>
        {#each uplinkResults as row}
          <tr>
            <td>{row.network}</td>
            <td>{row.interface}</td>
            <td>{row.serial}</td>
            <td>{(row.sent / 1_000_000).toFixed(1)}</td>
            <td>{(row.received / 1_000_000).toFixed(1)}</td>
            <td>{(row.total / 1_000_000).toFixed(1)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</main>
