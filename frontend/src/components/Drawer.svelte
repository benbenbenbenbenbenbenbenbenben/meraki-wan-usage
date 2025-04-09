<script lang="ts">
  import { fly } from "svelte/transition";
  import type { Snippet } from "svelte";
  import { drawers, toggleDrawer, closeDrawer } from "./usage.svelte";

  const open = $derived(() => drawers[id]?.open ?? false);
  const showBackdrop = $derived(() => drawers[id]?.showBackdrop ?? false);

  function handleToggle() {
    toggleDrawer(id);
  }

  let {
    id,
    btnName = "click",
    children,
  }: {
    id: string;
    btnName: string;
    children: Snippet;
  } = $props();
</script>

<button class="px-3" onclick={handleToggle}>
  {btnName}
</button>
{#if open()}
  {#key showBackdrop}
    {#if showBackdrop()}
      <button
        type="button"
        class="drawer-backdrop fade-in"
        onclick={handleToggle}
        data-id={id}
        aria-label="Close drawer"
      ></button>
    {/if}
  {/key}

  <div class="drawer" transition:fly={{ x: 400, duration: 250 }}>
    <button class="outline contrast" onclick={handleToggle}>X</button>
    {@render children()}
  </div>
{/if}

<style>
  .drawer-backdrop {
    all: unset;
    position: fixed;
    inset: 0;
    cursor: pointer;
    z-index: 999;
    background-color: rgba(0, 0, 0, 0);
    animation: fadeBackdropIn 250ms ease forwards;
  }

  @keyframes fadeBackdropIn {
    from {
      background-color: rgba(0, 0, 0, 0);
    }
    to {
      background-color: rgba(0, 0, 0, 0.4);
    }
  }

  .drawer {
    position: fixed;
    top: 0;
    right: 0;
    height: 100%;
    width: 600px;
    background: var(--pico-background-color);
    padding: 2rem;
    box-shadow: -2px 0 10px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transform: translateX(0);
    overflow-y: auto;
  }

  @media (max-width: 768px) {
    .drawer {
      width: 100%;
    }
  }
</style>
