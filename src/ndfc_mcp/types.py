"""Simplified return types for tool output.

These are what gets serialized and sent back to the LLM. Keep them flat
and human-readable — not 1:1 mirrors of the API response.
"""

from typing import Any

# Generic dict alias used when a tool returns a single resource
ResourceDict = dict[str, Any]

# Generic list alias used when a tool returns a collection
ResourceList = list[dict[str, Any]]
