#!/usr/bin/python
"""Pydantic input models for Audiobookshelf MCP API request parameters."""

from pydantic import BaseModel, Field


class LibraryItemsQueryInput(BaseModel):
    """Input model for paging/filtering library items."""

    limit: int | None = Field(default=None, description="Max items to return.")
    page: int | None = Field(default=None, description="Zero-based page index.")
    sort: str | None = Field(default=None, description="Sort key.")
    desc: int | None = Field(default=None, description="1 to sort descending.")
    filter: str | None = Field(
        default=None, description="Base64-encoded library filter expression."
    )


class AuthorMatchInput(BaseModel):
    """Input model for matching an author against a metadata provider."""

    q: str | None = Field(default=None, description="Author name to search for.")
    asin: str | None = Field(default=None, description="ASIN to match against.")
    region: str | None = Field(default=None, description="Metadata provider region.")
