<script lang="ts">
  import { getComparisonChartData } from "./usage.svelte";
  const chartData = getComparisonChartData();

  let max = $derived(() =>
    Math.max(...chartData().flatMap((d) => [d.primary ?? 0, d.compare ?? 0]))
  );
</script>

<div class="card-container">
  <div class="container">
    <div class="bar-chart">
      {#each chartData() as item}
        <div class="bar-row">
          <div class="bar-label">{item.label}</div>

          <div class="bar-wrapper-group">
            {#if item.primary !== undefined}
              <div class="bar-wrapper">
                <div
                  class="bar-fill bg-primary"
                  style="width: {(item.primary / max()) * 100}%"
                >
                  {item.primary}
                </div>
              </div>
            {/if}
            {#if item.compare !== undefined}
              <div class="bar-wrapper">
                <div
                  class="bar-fill bg-contrast"
                  style="width: {(item.compare / max()) * 100}%"
                >
                  {item.compare}
                </div>
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .bar-chart {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .bar-row {
    display: grid;
    grid-template-columns: 120px 1fr;
    align-items: start;
    column-gap: 1rem;
  }

  .bar-label {
    font-size: 0.75rem;
    font-weight: 300;
    text-align: right;
    white-space: nowrap;
    padding-top: 0.2rem;
  }

  .bar-wrapper-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .bar-wrapper {
    background: var(--pico-muted-border-color);
    height: 1.25rem;
    border-radius: var(--pico-border-radius);
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 0.5rem;
    color: white;
    font-size: 0.75rem;
    min-width: 40px;
    transition: width 0.6s ease;
    border-radius: var(--pico-border-radius);
  }

  .bg-primary {
    background-color: var(--pico-primary);
  }

  .bg-contrast {
    background-color: var(--pico-secondary);
  }
</style>
