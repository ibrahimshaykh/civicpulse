import { useEffect, useState } from "react";

/** Counts down from `seconds` to 0, ticking once per second. `null` disables it. */
export function useCountdown(seconds: number | null): number {
  const [remaining, setRemaining] = useState(seconds ?? 0);

  useEffect(() => {
    setRemaining(seconds ?? 0);
    if (seconds === null || seconds <= 0) return;
    const id = setInterval(() => {
      setRemaining((r) => Math.max(0, r - 1));
    }, 1000);
    return () => {
      clearInterval(id);
    };
  }, [seconds]);

  return remaining;
}
