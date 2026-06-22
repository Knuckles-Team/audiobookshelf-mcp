#!/usr/bin/python
"""Pydantic response models for Audiobookshelf MCP API payloads."""

from typing import Any

from pydantic import BaseModel, Field


class LibrariesResponse(BaseModel):
    """Response model for the list-libraries call."""

    libraries: list[dict[str, Any]] | None = Field(
        default=None, description="Configured libraries."
    )
    raw: dict[str, Any] | None = Field(
        default=None, description="Raw response payload."
    )
