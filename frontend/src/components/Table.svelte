<script lang="ts">
  import type { UplinkUsage } from "./types";
  import { formatValue } from "./usage.svelte";
  let { data }: { data: UplinkUsage[] } = $props();

  // Pagination
  let currentPage = $state(1);
  const itemsPerPage = 10;

  let totalPages = $derived.by(() => {
    return Math.ceil(data.length / itemsPerPage);
  });

  let paginatedRows = $derived.by(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return data.slice(start, start + itemsPerPage);
  });

  function goToPage(page: number) {
    if (page >= 1 && page <= totalPages) {
      currentPage = page;
    }
  }
</script>

<div class="card-container">
  <div class="table-data">
    <table role="grid">
      <thead>
        <tr>
          <th>Network</th>
          <th>Interface</th>
          <th>Serial</th>
          <th>Sent</th>
          <th>Received</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        {#each paginatedRows as row}
          <tr>
            <td>{row.networkName}</td>
            <td>{row.interface}</td>
            <td>{row.serial}</td>
            <td>{formatValue(row.sent)}</td>
            <td>{formatValue(row.received)}</td>
            <td>{formatValue(row.total)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
<!-- Pagination container -->
<div class="pagination-container">
  <nav class="pagination" aria-label="Page navigation">
    <ul>
      <li>
        <button
          class="contrast"
          onclick={() => goToPage(currentPage - 1)}
          disabled={currentPage === 1}
        >
          &laquo;
        </button>
      </li>

      {#each Array(totalPages) as _, index}
        <li>
          <button
            class:primary={index + 1 === currentPage}
            onclick={() => goToPage(index + 1)}
          >
            {index + 1}
          </button>
        </li>
      {/each}

      <li>
        <button
          class="contrast"
          onclick={() => goToPage(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          &raquo;
        </button>
      </li>
    </ul>
  </nav>
</div>

<style>
  .pagination-container {
    display: flex;
    justify-content: flex-end;
    padding: 0.5rem;
    background: var(--pico-card-background-color);
    border-radius: var(--pico-border-radius);
    box-shadow: var(--pico-card-box-shadow, 0 1px 2px rgba(0, 0, 0, 0.1));
    /* margin-top: 1rem; */
  }

  .pagination ul {
    display: flex;
    gap: 0.25rem;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .pagination li button {
    padding: 0.4rem 0.75rem;
  }
</style>
