#!/usr/bin/env python3
"""Wrapper for Chevron renderer. Opens provided template and renders document.
"""

from datetime import datetime
import chevron


def render(path_string: str, content: dict[str, str | datetime]) -> str:
    """Run Chevron renderer with provided template
    """
    with open(path_string, 'r', encoding='utf-8') as file:
        template: str = file.read()
    return chevron.render(template, content)
