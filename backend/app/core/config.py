from typing import Literal
from urllib.parse import quote

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # extra="ignore" means an env var meant for another service (e.g. compose's
    # POSTGRES_PASSWORD read by the postgres image itself) never fails startup.
    model_config = SettingsConfigDict(env_file=None, extra="ignore", case_sensitive=False)

    app_env: Literal["dev", "ci", "prod"] = "dev"
    app_version: str = "0.0.0"
    git_sha: str = "unknown"
    log_level: str = "INFO"

    postgres_host: str = "database"
    postgres_port: int = 5432
    postgres_db: str = "civicpulse"
    postgres_user: str = "civicpulse"
    postgres_password: SecretStr
    db_pool_size: int = 5
    db_max_overflow: int = 5
    db_pool_timeout_s: float = 5.0

    redis_host: str = "cache"
    redis_port: int = 6379
    redis_password: SecretStr
    redis_db: int = 0

    stats_cache_ttl_s: int = 30
    rate_limit_per_window: int = 10
    rate_limit_window_s: int = 60
    trusted_proxy_hops: int = 1  # nginx in compose; ingress in k8s

    triage_provider: Literal["llm", "ollama", "rules", "simulated"] = "rules"
    triage_timeout_s: float = 10.0
    triage_cache_ttl_s: int = 86_400
    groq_api_key: SecretStr | None = None
    groq_model: str = "llama-3.1-8b-instant"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "llama3.2:1b"
    simulated_failure_mode: Literal["none", "raise", "timeout", "malformed", "rate_limited"] = "none"
    simulated_seed: int = 42

    readiness_timeout_s: float = 1.0
    graceful_timeout_s: int = 20

    # repr=False: without it, Pydantic v2 includes computed fields in repr()/str()
    # by default, which would print the assembled URL -- password included in
    # plain text -- defeating the SecretStr fields above (this is what U10 tests).
    #
    # Built by hand rather than with sqlalchemy.URL: that import is banned outside
    # app/repositories and app/db (plan §10.1's layering rule), and it would be
    # a whole ORM dependency pulled into app/core just to format a string.
    @computed_field(repr=False)  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        user = quote(self.postgres_user, safe="")
        password = quote(self.postgres_password.get_secret_value(), safe="")
        return f"postgresql+asyncpg://{user}:{password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
