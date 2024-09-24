#!/usr/bin/env python3
"""Module for Slimeblogger HTML-generator class.
"""

import chevron


class BlogGenerator:
    """Class for containing template and accessing Chevron render
    """

    def __init__(self, path_string: str):
        self.template: str = self.open_template(path_string)

    def open_template(self, path_string: str) -> str:
        """Open template file, return contents
        """
        with open(path_string, 'r', encoding='utf-8') as file:
            return file.read()

    def generate_post(self, content: dict[str, str]) -> str:
        """Run Chevron renderer with saved template
        """
        return chevron.render(self.template, content)
