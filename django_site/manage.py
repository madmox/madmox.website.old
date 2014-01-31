#!/usr/bin/env python

if __name__ == "__main__":
    import os
    import sys
    
    from core.tools import set_env_vars
    projdir = os.path.dirname(os.path.abspath(__file__))
    set_env_vars(projdir)
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
