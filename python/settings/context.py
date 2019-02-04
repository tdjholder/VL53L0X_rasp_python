from contextlib import contextmanager
import os
from simple_settings import settings

ENV_KEY = 'settings'


@contextmanager
def settings_activator(env):
    """
    Set settings environment variable within context manager.
    :param env:
    :return:
    """
    settings._initialized = False;
    old_env = os.environ.get(ENV_KEY)
    os.environ[ENV_KEY] = env
    yield
    if old_env:
        os.environ[ENV_KEY] = old_env
    settings._initialized = False;