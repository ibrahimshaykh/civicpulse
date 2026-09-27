import { Navigate, type RouteObject } from "react-router-dom";

import { Layout } from "@/components/Layout";
import { RouteBoundary } from "@/components/RouteBoundary";
import { ComplaintDetailPage } from "@/pages/ComplaintDetailPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { NotFoundPage } from "@/pages/NotFoundPage";
import { StatsPage } from "@/pages/StatsPage";
import { SubmitPage } from "@/pages/SubmitPage";

// Kept apart from router.tsx so tests can mount the same tree in a memory router.
export const routes: RouteObject[] = [
  {
    element: <Layout />,
    children: [
      { index: true, element: <Navigate to="/submit" replace /> },
      { path: "submit", element: <RouteBoundary><SubmitPage /></RouteBoundary> },
      { path: "dashboard", element: <RouteBoundary><DashboardPage /></RouteBoundary> },
      { path: "complaints/:id", element: <RouteBoundary><ComplaintDetailPage /></RouteBoundary> },
      { path: "stats", element: <RouteBoundary><StatsPage /></RouteBoundary> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
];

// Opt in to v7 behaviour now so the upgrade is a no-op and tests stay free of warnings.
export const routerFuture = {
  v7_fetcherPersist: true,
  v7_normalizeFormMethod: true,
  v7_partialHydration: true,
  v7_relativeSplatPath: true,
  v7_skipActionErrorRevalidation: true,
} as const;
