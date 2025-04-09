<script>
  import OrgSelect from "./OrgSelect.svelte";
  import Drawer from "./Drawer.svelte";
  import Report from "./Report.svelte";
  import { usage } from "./usage.svelte";

  let showMenu = $state(false);

  let isDark = $state(false);
  let theme = "";
  function toggleTheme() {
    theme = isDark ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }

  // Load saved theme on mount
  if (typeof localStorage !== "undefined") {
    const saved = localStorage.getItem("theme");
    if (saved) {
      isDark = saved === "dark";
      document.documentElement.setAttribute("data-theme", saved);
    }
  }
</script>

<header>
  <nav class="container-fluid nav-bar">
    <ul class="nav-left">
      <li class="app-logo">
        <strong>WAN Usage</strong>
      </li>
    </ul>

    <ul class="nav-right">
      <li>
        <select bind:value={usage.unit}>
          <option value="MB">MB</option>
          <option value="GB">GB</option>
        </select>
      </li>
      <li>
        <Drawer id="report" btnName="Run Report"><OrgSelect /><Report /></Drawer
        >
      </li>
      <li>
        <span class="vertical-separator hide-mobile"></span>
      </li>
      <li class="github-link hide-mobile">
        <a
          href="https://github.com/benbenbenbenbenbenbenbenbenben/meraki-wan-usage"
          target="_blank"
          rel="noopener"
          aria-label="GitHub"
        >
          <img
            src="./github-mark.svg"
            alt="GitHub logo"
            width="36"
            height="36"
          />
        </a>
      </li>

      <li>
        <label class="theme-toggle hide-mobile">
          <input
            type="checkbox"
            bind:checked={isDark}
            onchange={toggleTheme}
            aria-label="Toggle dark mode"
          />
          <span class="track">
            <span class="thumb">{isDark ? "🌙" : "🌞"}</span>
          </span>
        </label>
      </li>
    </ul>
  </nav>
</header>

<style>
  .nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }

  .nav-bar ul {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .nav-left {
    flex: 1;
  }

  .nav-right {
    gap: 1rem;
  }

  .theme-toggle {
    position: relative;
    display: inline-block;
    width: 64px;
    height: 36px;
    vertical-align: middle;
  }

  .theme-toggle input {
    opacity: 0;
    width: 0;
    height: 0;
    position: absolute;
  }

  .track {
    background-color: #fce9a5; /* light default */
    border-radius: 50px;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    padding: 4px;
    box-sizing: border-box;
    transition: background-color 0.3s ease;
  }

  input:checked + .track {
    background-color: #0d3b66;
  }

  .thumb {
    background-color: #fbbc04;
    color: white;
    font-size: 18px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center; /* <-- vertical centering */
    justify-content: center;
    transform: translateX(0);
    transition:
      transform 0.3s ease,
      background-color 0.3s ease;
    flex-shrink: 0;
  }

  input:checked + .track .thumb {
    transform: translateX(28px);
    background-color: #3399ff;
  }

  .vertical-separator {
    display: inline-block;
    width: 1px;
    height: 1.5rem;
    background-color: var(--pico-muted-border-color);
    margin: 0 0.75rem;
  }

  .app-logo strong {
    font-size: 1.25rem;
    color: var(--pico-primary);
    font-weight: 600;
    letter-spacing: -1.5px;
    border-left: 4px solid var(--pico-primary);
    padding-left: 0.5rem;
  }

  @media (max-width: 768px) {
    .hide-mobile {
      display: none !important;
    }
  }
</style>
