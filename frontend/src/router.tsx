import { createBrowserRouter } from "react-router-dom";

import { routerFuture, routes } from "./routes";

export const router = createBrowserRouter(routes, { future: routerFuture });
