<script lang="ts">
  import { runReport, closeDrawer } from "./usage.svelte";

  let mode = $state("single-day");

  const today = new Date();
  const minSelectableDate = new Date(today);
  minSelectableDate.setDate(today.getDate() - 30);

  const formatDate = (d: Date) =>
    `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;

  function getWeekRange(endDate: Date) {
    const end = new Date(endDate);
    const start = new Date(end);
    start.setDate(end.getDate() - 6);
    return { start, end };
  }

  const addDays = (dateStr: string, days: number) => {
    const d = new Date(dateStr);
    d.setDate(d.getDate() + days);
    return formatDate(d);
  };

  // $effect: ensure end dates auto-calculate
  $effect(() => {
    selectedWeekEnd = addDays(selectedWeekStart, 6);
  });

  $effect(() => {
    compareWeek1End = addDays(compareWeek1Start, 6);
  });

  // Limit max week start to today - 6
  const maxWeekStart = new Date(today);
  maxWeekStart.setDate(today.getDate() - 6);
  const maxWeekStartStr = formatDate(maxWeekStart);

  // Prefilled ranges
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const dayBeforeYesterday = new Date(today);
  dayBeforeYesterday.setDate(today.getDate() - 2);

  const lastWeekEnd = new Date(today);
  lastWeekEnd.setDate(today.getDate() - today.getDay());
  const lastWeek = getWeekRange(lastWeekEnd);

  const prevWeekEnd = new Date(lastWeek.start);
  prevWeekEnd.setDate(prevWeekEnd.getDate() - 1);
  const prevWeek = getWeekRange(prevWeekEnd);

  const lastMonthStart = new Date(today);
  lastMonthStart.setDate(today.getDate() - 30);

  // $state values
  let selectedDate = $state(formatDate(yesterday));
  let compareDate1 = $state(formatDate(dayBeforeYesterday));
  let compareDate2 = $state(formatDate(yesterday));
  let selectedWeekStart = $state(formatDate(lastWeek.start));
  let selectedWeekEnd = $state(formatDate(lastWeek.end));
  let compareWeek1Start = $state(formatDate(prevWeek.start));
  let compareWeek1End = $state(formatDate(prevWeek.end));

  let errorMessage = $state("");
  let isLoading = $state(false);
  let isSuccess = $state(false);
  let progress = $state(0);
  let showDelayMessage = $state(false);
  let progressInterval: number;
  let delayMessageTimeout: number;

  async function onRun() {
    errorMessage = "";
    isLoading = true;
    isSuccess = false;
    showDelayMessage = false;
    progress = 10;

    // Simulated progress increase up to 85%
    let simulatedProgress = 10;
    progressInterval = window.setInterval(() => {
      if (simulatedProgress < 85) {
        simulatedProgress += 5;
        progress = simulatedProgress;
      }
    }, 1000); // every 1 second

    // Show delay message after 5 seconds
    delayMessageTimeout = window.setTimeout(() => {
      showDelayMessage = true;
    }, 5000);

    try {
      await runReport({
        mode,
        selectedDate,
        compareDate1,
        compareDate2,
        selectedWeekStart,
        selectedWeekEnd,
        compareWeek1Start,
        compareWeek1End,
        last30Start: formatDate(lastMonthStart),
        last30End: formatDate(today),
      });

      clearInterval(progressInterval);
      clearTimeout(delayMessageTimeout);
      progress = 100;
      isSuccess = true;

      setTimeout(() => {
        isLoading = false;
        progress = 0;
        showDelayMessage = false;
        closeDrawer("report");
      }, 500);
    } catch (err) {
      clearInterval(progressInterval);
      clearTimeout(delayMessageTimeout);
      errorMessage = `Failed to fetch report. Please try again. ${err}`;
      isLoading = false;
      showDelayMessage = false;
      progress = 0;
    }
  }
</script>

<section>
  <hgroup>
    <h2>Select Dates</h2>
    <p>Choose a date range or comparison</p>
  </hgroup>

  {#if errorMessage}
    <article class="pico-background-pink-600">{errorMessage}</article>
  {/if}

  <fieldset>
    <legend>Mode</legend>
    <label>
      <input type="radio" name="mode" value="single-day" bind:group={mode} />
      Day
    </label>
    <label>
      <input type="radio" name="mode" value="compare-days" bind:group={mode} />
      Compare Days
    </label>
    <label>
      <input type="radio" name="mode" value="week" bind:group={mode} />
      Week
    </label>
    <label>
      <input type="radio" name="mode" value="compare-weeks" bind:group={mode} />
      Compare Weeks
    </label>
    <label>
      <input type="radio" name="mode" value="month" bind:group={mode} />
      Last 30 Days
    </label>
  </fieldset>

  {#if mode === "single-day"}
    <input
      type="date"
      bind:value={selectedDate}
      max={formatDate(today)}
      min={formatDate(minSelectableDate)}
    />
  {:else if mode === "compare-days"}
    <div class="grid">
      <input
        type="date"
        bind:value={compareDate1}
        max={formatDate(today)}
        min={formatDate(minSelectableDate)}
      />
      <input
        type="date"
        bind:value={compareDate2}
        max={formatDate(today)}
        min={formatDate(minSelectableDate)}
      />
    </div>
  {:else if mode === "week"}
    <div class="grid">
      <label>
        Start
        <input
          type="date"
          bind:value={selectedWeekStart}
          max={maxWeekStartStr}
        />
      </label>
      <label>
        End
        <input type="date" value={selectedWeekEnd} disabled />
      </label>
    </div>
  {:else if mode === "compare-weeks"}
    <div class="grid">
      <label>
        Start
        <input
          type="date"
          bind:value={compareWeek1Start}
          max={maxWeekStartStr}
        />
      </label>
      <label>
        End
        <input type="date" value={compareWeek1End} disabled />
      </label>
    </div>
    <div class="grid">
      <label>
        Start
        <input
          type="date"
          bind:value={selectedWeekStart}
          max={maxWeekStartStr}
        />
      </label>
      <label>
        End
        <input type="date" value={selectedWeekEnd} disabled />
      </label>
    </div>
  {/if}

  <button
    type="button"
    class="my-4"
    onclick={onRun}
    disabled={isLoading}
    data-loading={isLoading ? "true" : undefined}
  >
    {#if isLoading}
      Loading...
    {:else}
      Run Report
    {/if}
  </button>

  {#if isLoading}
    <progress value={progress} max="100"></progress>
    {#if showDelayMessage}
      <p class="dim mt-2">
        Still working... this may take a few more seconds ⏳
      </p>
    {/if}
  {/if}
</section>

<style>
  .my-4 {
    margin: 1rem 0;
  }
</style>
