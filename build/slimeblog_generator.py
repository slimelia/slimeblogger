#!/usr/bin/env python3
"""Module for Slimeblogger HTML-generator class.
"""

import chevron


class BlogGenerator:
    """Class for containing template and accessing Chevron render
    """

    def __init__(self, path_string: str):
        self._template: str = self._open_template(path_string)

    def _open_template(self, path_string: str) -> str:
        """Open template file, return contents
        """
        with open(path_string, 'r', encoding='utf-8') as file:
            return file.read()

    def generate_page(self, content: dict[str, str]) -> str:
        """Run Chevron renderer with saved template
        """
        return chevron.render(self._template, content)
