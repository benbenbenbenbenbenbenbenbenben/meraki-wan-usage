<script lang="ts">
  import { Tween } from "svelte/motion";
  import { cubicOut } from "svelte/easing";

  import { formatValueLabel } from "./usage.svelte";

  let {
    totalUsageData,
    avgUsageData,
    interfaceSpread,
    compareTotalUsageData,
    compareAvgUsageData,
  }: {
    totalUsageData: number;
    avgUsageData: number;
    interfaceSpread: {
      interface: string;
      total: number;
      percent: number;
    }[];
    compareTotalUsageData?: number;
    compareAvgUsageData?: number;
  } = $props();

  const interfaceColors: Record<string, string> = {
    wan1: "#3b82f6", // blue
    wan2: "#f59e0b", // amber
    cellular: "#10b981", // green
    unknown: "#d1d5db", // gray
  };

  let totalUsage = new Tween(0, {
    duration: 400,
    easing: cubicOut,
  });

  let avgUsage = new Tween(0, {
    duration: 400,
    easing: cubicOut,
  });

  let compareTotalUsage = new Tween(0, {
    duration: 400,
    easing: cubicOut,
  });

  let compareAvgUsage = new Tween(0, {
    duration: 400,
    easing: cubicOut,
  });

  let pieStyle = $state(buildPieGradient(interfaceSpread));

  $effect(() => {
    totalUsage.target = totalUsageData;
    avgUsage.target = avgUsageData;
    if (compareTotalUsageData !== undefined) {
      compareTotalUsage.target = compareTotalUsageData;
    }

    if (compareAvgUsageData !== undefined) {
      compareAvgUsage.target = compareAvgUsageData;
    }
    pieStyle = buildPieGradient(interfaceSpread);
  });

  function buildPieGradient(data) {
    let current = 0;
    const segments = [];

    for (const entry of data) {
      const start = current;
      const end = current + entry.percent;
      const color = interfaceColors[entry.interface] ?? interfaceColors.unknown;
      segments.push(`${color} ${start}% ${end}%`);
      current = end;
    }

    return `conic-gradient(${segments.join(", ")})`;
  }
</script>

<div class="grid">
  <article>
    <header>
      <h4>Total Usage</h4>
    </header>
    <div class="usage-row">
      <h2>{formatValueLabel(totalUsage.current)}</h2>

      {#if compareTotalUsageData !== undefined}
        <div class="compare-block">
          <span class="divider" aria-hidden="true"></span>
          <div class="compare-values">
            <h2 class="compare">
              {formatValueLabel(compareTotalUsage.current)}
            </h2>
            <p
              class="delta {compareTotalUsage.current > totalUsage.current
                ? 'increase'
                : 'decrease'}"
            >
              {formatValueLabel(compareTotalUsage.current - totalUsage.current)}
              difference
            </p>
          </div>
        </div>
      {/if}
    </div>
    <p>All networks combined</p>
  </article>

  <article>
    <header>
      <h4>Average Usage</h4>
    </header>
    <div class="usage-row">
      <h2>{formatValueLabel(avgUsage.current)}</h2>

      {#if compareAvgUsageData !== undefined}
        <div class="compare-block">
          <span class="divider" aria-hidden="true"></span>
          <div class="compare-values">
            <h2 class="compare">{formatValueLabel(compareAvgUsage.current)}</h2>
            <p
              class="delta {compareAvgUsage.current > avgUsage.current
                ? 'increase'
                : 'decrease'}"
            >
              {formatValueLabel(compareAvgUsage.current - avgUsage.current)} difference
            </p>
          </div>
        </div>
      {/if}
    </div>
    <p>Per network</p>
  </article>

  <article>
    <header>
      <h4>Interface Spread</h4>
    </header>

    <div class="pie-chart-container">
      <div class="pie" style="background: {pieStyle};"></div>
      <ul class="pie-legend">
        {#each interfaceSpread as item}
          <li>
            <span
              class="swatch"
              style="background-color: {interfaceColors[item.interface] ??
                interfaceColors.unknown}"
            ></span>
            {item.interface.toUpperCase()} – {Math.round(item.percent)}%
          </li>
        {/each}
      </ul>
    </div>
  </article>
</div>

<style>
  .usage-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }

  .usage-row h2 {
    margin: 0;
  }

  .compare-block {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .divider {
    width: 1px;
    height: 2.5rem;
    background: var(--pico-muted-border-color);
    display: inline-block;
  }

  .compare-values {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .compare {
    color: var(--pico-muted-color);
    font-weight: 400;
    font-size: 1.15rem;
    margin: 0;
  }

  .delta {
    font-size: 0.75rem;
    margin: 0;
    padding-top: 2px;
  }

  .delta.increase {
    color: var(--pico-del-color, #e63946); /* red */
  }

  .delta.decrease {
    color: var(--pico-ok-color, #2a9d8f); /* green */
  }

  .pie-chart-container {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }

  .pie {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(gray 0% 100%);
    transition: background 0.7s ease;
    box-shadow: 0 0 0 1px var(--pico-muted-border-color);
  }

  .pie-legend {
    list-style: none;
    padding-left: 0;
    font-size: 0.85rem;
    display: flex;
    flex-direction: column;
    gap: 0rem;
  }

  .pie-legend li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .swatch {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 0 1px var(--pico-muted-border-color);
  }
</style>
