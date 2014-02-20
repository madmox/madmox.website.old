import os
from django.core.exceptions import ImproperlyConfigured


def get_env_var(key, required=True, default=None):
    """
    Gets the setting corresponding to the given key and returns it.
    
    If the matching environment is not defined and the setting is marked
    as required, raises an ImproperlyConfigured exception.
    
    """
    if required:
        try:
            return os.environ[key]
        except KeyError:
            raise ImproperlyConfigured("Missing setting '{0}'".format(key))
    else:
        return os.environ.get(key, default)


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
