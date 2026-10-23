# ADR 0002: Frontend Runtime Config
**Decision:** Serve API through Nginx proxy `/api` via envsubst.
**Rationale:** Prevents baking API URLs into the image, adhering to build-once-deploy-many.
