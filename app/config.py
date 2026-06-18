"""Configuration for the signal engine."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_mode: str = Field("mock", alias="LLM_MODE")            # mock | azure
    signal_source: str = Field("mock", alias="SIGNAL_SOURCE")  # mock | api
    # Weight per signal type when scoring how 'hot' a company is.
    hot_threshold: float = Field(6.0, alias="HOT_THRESHOLD")
    targets_csv: str = Field("data/targets.csv", alias="TARGETS_CSV")

    # Azure (only if llm_mode=azure)
    azure_openai_endpoint: str | None = Field(None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = Field(None, alias="AZURE_OPENAI_API_KEY")
    azure_deployment: str = Field("gpt-4o", alias="AZURE_DEPLOYMENT")
    azure_api_version: str = Field("2024-10-21", alias="AZURE_API_VERSION")


settings = Settings()

# Signal type -> base weight. Funding/leadership moves are the strongest buy signals.
SIGNAL_WEIGHTS = {
    "funding_round": 4.0,
    "leadership_change": 3.0,
    "acquisition": 3.5,
    "hiring_spike": 2.0,
    "product_launch": 1.5,
    "news_mention": 1.0,
}
