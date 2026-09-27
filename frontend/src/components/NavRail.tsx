import { NavLink } from "react-router-dom";

const ITEMS = [
  { to: "/submit", label: "Submit" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/stats", label: "Stats" },
] as const;

// Left rail on wide screens, top bar under 768 px. The active item carries the
// hi-vis signal bar; NavLink also sets aria-current="page" for screen readers.
export function NavRail() {
  return (
    <nav aria-label="Main" className="bg-ink text-paper md:min-h-screen md:w-48 md:shrink-0">
      <p className="px-4 py-4 text-lg font-semibold tracking-tight">CivicPulse</p>
      <ul className="flex md:flex-col">
        {ITEMS.map((item) => (
          <li key={item.to}>
            <NavLink
              to={item.to}
              className={({ isActive }) =>
                [
                  "block border-b-4 px-4 py-3 text-base md:border-b-0 md:border-l-4",
                  isActive ? "border-signal font-semibold" : "border-transparent hover:bg-white/10",
                ].join(" ")
              }
            >
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
