#!/usr/bin/env python3

import chevron


def render(path_string: str, content: dict[str, str]) -> str:
    """Run Chevron renderer with provided template
    """
    with open(path_string, 'r', encoding='utf-8') as file:
        template: str = file.read()
    return chevron.render(template, content)
