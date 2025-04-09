<script lang="ts">
  import { onMount } from "svelte";
  let modalTitle = "";
  let modalMessage = "";
  let showModal = false;

  function closeModal() {
    const dialog = document.getElementById("apiKeyModal") as HTMLDialogElement;
    if (dialog) dialog.close();
  }

  function openModal() {
    const dialog = document.getElementById(
      "apiKeyModal"
    ) as HTMLDialogElement | null;
    if (dialog && !dialog.open) {
      dialog.showModal();
    }
  }

  onMount(async () => {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();

      if (data.status !== "ok") {
        modalTitle = data.title;
        modalMessage = data.message;
        openModal();
      }
    } catch (e) {
      modalTitle = "Server Error";
      modalMessage = "Something went wrong checking API key status.";
      openModal();
    }
  });
</script>

<dialog id="apiKeyModal" class="modal">
  <article>
    <header>
      <h3>{modalTitle}</h3>
    </header>
    <p>{modalMessage}</p>
    <footer>
      <button class="secondary" onclick={() => closeModal()}>Close</button>
    </footer>
  </article>
</dialog>
