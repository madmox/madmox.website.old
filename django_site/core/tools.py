import os


def set_env_vars(projdir, envdir='envdir'):
    """
    Sets environment variables from the contents of '{projdir}/{envdir}'
    directory
    """
    env_dir = os.path.abspath(os.path.join(projdir, envdir))
    env_var_names = [ x for x in os.listdir(env_dir) if not x.startswith('_') ]
    for env_var_name in env_var_names:
        env_file_path = os.path.join(env_dir, env_var_name)
        with open(env_file_path, 'r') as env_file:
            env_var_value = env_file.read().strip()
            os.environ.setdefault(env_var_name, env_var_value)
