#!/usr/bin/env python
"""Vercel-compatible Django entry point.

The application package lives in ``campus_solve_ai/``.  Keeping this wrapper
at the repository root lets Vercel identify the project as Django while the
original package-level management script continues to work locally.
"""
import os
import sys


def main():
    settings_module = (
        'campus_solve_ai.settings.production'
        if os.getenv('VERCEL')
        else 'campus_solve_ai.settings'
    )
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
