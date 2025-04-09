<script lang="ts">
  import { onMount } from "svelte";
  import { usage } from "./usage.svelte";

  let organizations = $state<{ id: string; name: string }[]>([]);
  let error = $state("");

  onMount(async () => {
    try {
      const res = await fetch("/api/organizations");
      organizations = await res.json();
      const saved = usage.selectedOrg;

      // Check if saved org is in the fetched list
      const isValid = organizations.some(
        (org: { id: string }) => org.id === saved
      );

      usage.selectedOrg = isValid ? saved : organizations[0].id;
      usage.selectedOrgName = organizations[0].name;
    } catch (e) {
      error = "Failed to load organizations.";
    }
  });

  $effect(() => {
    const selected = organizations.find((org) => org.id === usage.selectedOrg);
    if (selected) {
      usage.selectedOrgName = selected.name;
      localStorage.setItem("selectedOrgName", usage.selectedOrgName);
    }
  });
</script>

<hgroup>
  <h3>Organization Settings</h3>
  <p>Select an organization to report on.</p>
</hgroup>
<select
  name="selectOrg"
  aria-label="Select Org"
  required
  bind:value={usage.selectedOrg}
>
  <option disabled selected value="">Select Organization</option>
  {#each organizations as org}
    <option value={org.id}>{org.name}</option>
  {/each}
</select>

{#if error}
  <p class="error">{error}</p>
{/if}
