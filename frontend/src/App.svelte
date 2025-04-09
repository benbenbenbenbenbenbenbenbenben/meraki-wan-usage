<script lang="ts">
  import { onMount } from "svelte";
  import Chart from "./components/Chart.svelte";
  import Header from "./components/Header.svelte";
  import Footer from "./components/Footer.svelte";
  import MetricCards from "./components/MetricCards.svelte";
  import Table from "./components/Table.svelte";
  import KeyModel from "./components/KeyModel.svelte";

  import {
    usage,
    reportParams,
    getFilterData,
    getFilteredAvg,
    getFilteredTotal,
    getFilteredAvgCompare,
    getFilteredTotalCompare,
    getAvailableTags,
    getInterfaceSpread,
  } from "./components/usage.svelte";

  $effect(() => {
    if (usage.selectedOrg) {
      localStorage.setItem("selectedOrg", usage.selectedOrg);
    }
  });

  // onMount(fetchUplinksTest);
</script>

<!-- PicoCSS Table + Controls -->
<Header />
<main class="container">
  <hgroup>
    <h2>{usage.selectedOrgName}</h2>

    <p>
      {#if reportParams.report?.mode === "single-day"}
        {reportParams.report.data.date}
      {:else if reportParams.report.mode === "month" || reportParams.report.mode === "week"}
        {reportParams.report.data.start} — {reportParams.report.data.end}
      {:else if reportParams.report.mode === "compare-days"}
        {reportParams.report.data.dates[0]} vs {reportParams.report.data
          .dates[1]}
      {:else if reportParams.report.mode === "compare-weeks"}
        {reportParams.report.data.weeks[0].start} — {reportParams.report.data
          .weeks[0].end}
        vs
        {reportParams.report.data.weeks[1].start} — {reportParams.report.data
          .weeks[1].end}
      {/if}
    </p>
  </hgroup>
  <MetricCards
    totalUsageData={getFilteredTotal()}
    avgUsageData={getFilteredAvg()}
    interfaceSpread={getInterfaceSpread()}
    {...getFilteredTotalCompare() && {
      compareTotalUsageData: getFilteredTotalCompare(),
    }}
    {...getFilteredAvgCompare() && {
      compareAvgUsageData: getFilteredAvgCompare(),
    }}
  />
  <div class="grid">
    <input
      type="text"
      placeholder="Filter by network name..."
      bind:value={usage.filters.filterText}
      class="border p-2 mb-4 rounded"
    />
    <select bind:value={usage.filters.tag}>
      <option value="all">All Tags</option>
      {#each getAvailableTags() as tag}
        <option value={tag}>{tag}</option>
      {/each}
    </select>

    <select
      bind:value={usage.filters.selectedInterface}
      class="border p-2 rounded"
    >
      <option value="all">All Interfaces</option>
      <option value="wan1">wan1</option>
      <option value="wan2">wan2</option>
      <option value="cellular">cellular</option>
    </select>

    <select bind:value={usage.filters.sortBy} class="border p-2 w-full rounded">
      <option value="total">Sort by Total</option>
      <option value="sent">Sort by Sent</option>
      <option value="received">Sort by Received</option>
    </select>
  </div>

  <Chart />

  <Table data={getFilterData()} />
  <KeyModel />
</main>
<Footer />
