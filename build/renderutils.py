#!/usr/bin/env python3
"""Wrapper for Chevron renderer. Opens provided template and renders document.
"""

import chevron


def render(path_string: str, content: dict[str, str | None]) -> str:
    """Run Chevron renderer with provided template
    """
    with open(path_string, 'r', encoding='utf-8') as file:
        template: str = file.read()
    return chevron.render(template, content)
