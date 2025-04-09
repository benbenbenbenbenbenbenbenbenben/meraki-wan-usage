export type UplinkUsage = {
  networkId: string;
  networkName: string;
  interface: "wan1" | "wan2" | "cellular";
  serial: string;
  sent: number;
  received: number;
  total: number;
  tags?: string[];
};

export type DateParams =
  | { mode: "single-day"; data: { date: string } }
  | { mode: "month"; data: { start: string; end: string } } // Last 30 days
  | { mode: "week"; data: { start: string; end: string } } // Custom week
  | { mode: "compare-days"; data: { dates: [string, string] } }
  | {
      mode: "compare-weeks";
      data: {
        weeks: [{ start: string; end: string }, { start: string; end: string }];
      };
    };
