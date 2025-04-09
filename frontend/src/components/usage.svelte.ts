import type { UplinkUsage, DateParams } from "./types";

export const usage = $state<{
  data: UplinkUsage[];
  selectedOrg: string;
  selectedOrgName: string;
  unit: "MB" | "GB";
  filters: {
    filterText: string;
    selectedInterface: "all" | "wan1" | "wan2" | "cellular";
    sortBy: "total" | "sent" | "received";
    sortDesc: boolean;
    tag: string;
  };
}>({
  data: [],
  selectedOrg: localStorage.getItem("selectedOrg") ?? "",
  selectedOrgName: localStorage.getItem("selectedOrgName") ?? "",
  unit: "GB",
  filters: {
    filterText: "",
    selectedInterface: "all",
    sortBy: "total",
    sortDesc: true,
    tag: "all",
  },
});

const today = new Date();
// Yesterday
const yesterday = new Date(today);
yesterday.setDate(today.getDate() - 1);

// Format helpers
const formatDate = (d: Date) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
    d.getDate()
  ).padStart(2, "0")}`;

let selectedDate = formatDate(yesterday);

export const reportParams = $state<{
  report: DateParams;
}>({
  mode: "single-day",
  data: {
    date: selectedDate,
  },
});

reportParams.report = {
  mode: "single-day",
  data: {
    date: selectedDate,
  },
};

export const compareUsage = $state<UplinkUsage[]>([]);

export function formatValueLabel(bytes: number): string {
  const unit = usage.unit;
  if (unit === "GB") {
    return (bytes / 1_000_000_000).toFixed(2) + " GB";
  }
  // Default to MB
  return (bytes / 1_000_000).toFixed(0) + " MB";
}

export function formatValue(bytes: number): number {
  return usage.unit === "GB"
    ? +(bytes / 1_000_000_000).toFixed(2)
    : +(bytes / 1_000_000).toFixed(0);
}

const filteredData = $derived.by(() => {
  return usage.data
    .filter(
      (n) =>
        n.networkName
          .toLowerCase()
          .includes(usage.filters.filterText.toLowerCase()) &&
        (usage.filters.selectedInterface === "all" ||
          n.interface === usage.filters.selectedInterface) &&
        (usage.filters.tag === "all" || n.tags?.includes(usage.filters.tag))
    )
    .map((n) => ({
      ...n,
      total: n.sent + n.received,
    }))
    .sort((a, b) => {
      const diff = a[usage.filters.sortBy] - b[usage.filters.sortBy];
      return usage.filters.sortDesc ? -diff : diff;
    });
});

const filteredCompareData = $derived.by(() => {
  return compareUsage
    .filter(
      (n) =>
        n.networkName
          .toLowerCase()
          .includes(usage.filters.filterText.toLowerCase()) &&
        (usage.filters.selectedInterface === "all" ||
          n.interface === usage.filters.selectedInterface) &&
        (usage.filters.tag === "all" || n.tags?.includes(usage.filters.tag))
    )
    .map((n) => ({
      ...n,
      total: n.sent + n.received,
    }))
    .sort((a, b) => {
      const diff = a[usage.filters.sortBy] - b[usage.filters.sortBy];
      return usage.filters.sortDesc ? -diff : diff;
    });
});

const totalUsage = $derived.by(() => {
  return filteredData.reduce((sum, d) => sum + d.total, 0);
});

const avgUsage = $derived.by(() => {
  return filteredData.length ? totalUsage / filteredData.length : 0;
});

const totalUsageCompare = $derived.by(() => {
  return filteredCompareData.reduce((sum, d) => sum + d.total, 0);
});

const avgUsageCompare = $derived.by(() => {
  return filteredCompareData.length
    ? totalUsageCompare / filteredCompareData.length
    : 0;
});

const availableTags = $derived.by(() => {
  const allTags = usage.data.flatMap((n) => n.tags || []);
  return Array.from(new Set(allTags)).sort();
});

const interfaceSpread = $derived.by(() => {
  const spreadMap: Record<string, number> = {};

  for (const row of filteredData) {
    const iface = row.interface || "unknown";
    const total = row.sent + row.received;

    spreadMap[iface] = (spreadMap[iface] || 0) + total;
  }

  const grandTotal = Object.values(spreadMap).reduce((a, b) => a + b, 0);

  return Object.entries(spreadMap)
    .map(([iface, total]) => ({
      interface: iface,
      total,
      percent: grandTotal ? (total / grandTotal) * 100 : 0,
    }))
    .sort((a, b) => b.total - a.total); // Optional: sort descending
});

const comparisonChartData = $derived(() => {
  const primary = filteredData;
  const compare = filteredCompareData;

  const map = new Map<
    string,
    { label: string; primary?: number; compare?: number }
  >();

  for (const row of primary) {
    const label = `${row.networkName} - ${row.interface}`;
    map.set(label, {
      label,
      primary: formatValue(row.total),
    });
  }

  for (const row of compare) {
    const label = `${row.networkName} - ${row.interface}`;
    const existing = map.get(label) || { label };
    existing.compare = formatValue(row.total);
    map.set(label, existing);
  }

  return Array.from(map.values());
});

export async function fetchUplinksTest() {
  const response = await fetch("/api/test_data");
  const json = await response.json();

  for (const record of json) {
    for (const uplink of record.byUplink || []) {
      usage.data.push({
        networkId: record.networkId,
        networkName: record.name,
        interface: uplink.interface,
        serial: uplink.serial,
        sent: uplink.sent,
        received: uplink.received,
        total: uplink.sent + uplink.received,
      });
    }
  }
}

export async function fetchUplinks(orgId: string) {
  const response = await fetch(`/api/meraki/uplinks/${orgId}?period=day`);
  const json = await response.json();
  usage.data.length = 0;
  for (const record of json) {
    for (const uplink of record.byUplink || []) {
      usage.data.push({
        networkId: record.networkId,
        networkName: record.name,
        interface: uplink.interface,
        serial: uplink.serial,
        sent: uplink.sent,
        received: uplink.received,
        total: uplink.sent + uplink.received,
      });
    }
  }
}

export async function fetchUplinksForParams(orgId: string, params: DateParams) {
  const queryParams = new URLSearchParams();

  queryParams.set("mode", params.mode);

  switch (params.mode) {
    case "single-day":
      queryParams.set("date", params.data.date);
      break;

    case "month":
      queryParams.set("start", params.data.start);
      queryParams.set("end", params.data.end);
      break;

    case "week":
      queryParams.set("start", params.data.start);
      queryParams.set("end", params.data.end);
      break;

    case "compare-days":
      queryParams.set("dates", params.data.dates.join(","));
      break;

    case "compare-weeks":
      const weekStrings = params.data.weeks.flatMap((w) => [w.start, w.end]);
      queryParams.set("weeks", weekStrings.join(","));
      break;
  }
  const url = `/api/meraki/uplinks/${orgId}?${queryParams.toString()}`;

  const response = await fetch(url);

  if (params.mode.startsWith("compare-")) {
    const { primary, compare } = await response.json();

    usage.data.length = 0;
    for (const record of primary) {
      for (const uplink of record.byUplink || []) {
        usage.data.push({
          networkId: record.networkId,
          networkName: record.name,
          interface: uplink.interface,
          serial: uplink.serial,
          sent: uplink.sent,
          received: uplink.received,
          total: uplink.sent + uplink.received,
          tags: record.tags || [],
        });
      }
    }

    compareUsage.length = 0;
    for (const record of compare) {
      for (const uplink of record.byUplink || []) {
        compareUsage.push({
          networkId: record.networkId,
          networkName: record.name,
          interface: uplink.interface,
          serial: uplink.serial,
          sent: uplink.sent,
          received: uplink.received,
          total: uplink.sent + uplink.received,
          tags: record.tags || [],
        });
      }
    }
  } else {
    const json = await response.json();

    usage.data.length = 0;
    for (const record of json) {
      for (const uplink of record.byUplink || []) {
        usage.data.push({
          networkId: record.networkId,
          networkName: record.name,
          interface: uplink.interface,
          serial: uplink.serial,
          sent: uplink.sent,
          received: uplink.received,
          total: uplink.sent + uplink.received,
          tags: record.tags || [],
        });
      }
    }
    compareUsage.length = 0;
  }
}

export function getFilterData() {
  return filteredData;
}
// export function getChartData() {
//   return chartData;
// }

export function getComparisonChartData() {
  return comparisonChartData;
}

export function getFilteredAvg() {
  return avgUsage;
}

export function getFilteredTotal() {
  return totalUsage;
}

export function getFilteredAvgCompare() {
  return avgUsageCompare;
}

export function getFilteredTotalCompare() {
  return totalUsageCompare;
}

export function getAvailableTags() {
  return availableTags;
}

export function getInterfaceSpread() {
  return interfaceSpread;
}

export const drawers = $state<
  Record<string, { open: boolean; showBackdrop: boolean }>
>({});

export function toggleDrawer(id: string) {
  const current = drawers[id] ?? { open: false, showBackdrop: false };

  if (current.open) {
    document.body.style.overflow = "auto"; // Restore scroll
  } else {
    document.body.style.overflow = "hidden"; // Lock scroll
  }

  // Optionally handle the backdrop animation here
  if (current.open) {
    const backdrop = document.querySelector(
      `.drawer-backdrop[data-id="${id}"]`
    );
    if (backdrop) {
      backdrop.classList.remove("fade-in");
      backdrop.classList.add("fade-out");
    }
  }

  drawers[id] = {
    open: !current.open,
    showBackdrop: !current.showBackdrop,
  };
}

export function openDrawer(id: string) {
  drawers[id] = { open: true, showBackdrop: true };
}

export function closeDrawer(id: string) {
  drawers[id] = { open: false, showBackdrop: false };
  document.body.style.overflow = "auto";
}

export function isDrawerOpen(id: string): boolean {
  return drawers[id]?.open ?? false;
}

export async function runReport({
  mode,
  selectedDate,
  last30Start,
  last30End,
  selectedWeekStart,
  selectedWeekEnd,
  compareDate1,
  compareDate2,
  compareWeek1Start,
  compareWeek1End,
}: {
  mode: DateParams["mode"];
  selectedDate?: string;
  last30Start?: string;
  last30End?: string;
  selectedWeekStart?: string;
  selectedWeekEnd?: string;
  compareDate1?: string;
  compareDate2?: string;
  compareWeek1Start?: string;
  compareWeek1End?: string;
}) {
  const params: DateParams =
    mode === "single-day"
      ? { mode, data: { date: selectedDate! } }
      : mode === "month"
      ? { mode, data: { start: last30Start!, end: last30End! } }
      : mode === "week"
      ? { mode, data: { start: selectedWeekStart!, end: selectedWeekEnd! } }
      : mode === "compare-days"
      ? { mode, data: { dates: [compareDate1!, compareDate2!] } }
      : {
          mode,
          data: {
            weeks: [
              { start: compareWeek1Start!, end: compareWeek1End! },
              { start: selectedWeekStart!, end: selectedWeekEnd! },
            ],
          },
        };

  reportParams.report = params;

  if (usage.selectedOrg) {
    await fetchUplinksForParams(usage.selectedOrg, params);
  }
}
