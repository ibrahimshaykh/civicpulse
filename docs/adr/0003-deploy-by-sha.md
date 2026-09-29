# ADR 0003: Deploy by SHA
**Decision:** Deploy images pinned by commit SHA.
**Rationale:** `:latest` is mutable and prevents reliable rollbacks. SHA ensures exact code versions are deployed.
