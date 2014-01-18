#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    env_dir = 'envdir'
    env_var_names = [ x for x in os.listdir(env_dir) if not x.startswith('_') ]
    for env_var_name in env_var_names:
        env_file_path = os.path.join(env_dir, env_var_name)
        with open(env_file_path, 'r') as env_file:
            env_var_value = env_file.read().strip()
            os.environ.setdefault(env_var_name, env_var_value)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
