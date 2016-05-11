#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    print 'Let\'s try using python -m django [command] from now on'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bogg.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
