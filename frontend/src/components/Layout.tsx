import { Outlet } from "react-router-dom";

import { NavRail } from "./NavRail";

export function Layout() {
  return (
    <div className="min-h-screen md:flex">
      <a
        href="#content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-10 focus:bg-signal focus:px-3 focus:py-2 focus:text-ink"
      >
        Skip to content
      </a>
      <NavRail />
      <main id="content" tabIndex={-1} className="flex-1 px-4 py-8 md:px-10">
        <Outlet />
      </main>
    </div>
  );
}
