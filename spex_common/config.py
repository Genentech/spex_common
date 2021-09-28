from os import path, environ, getcwd
from dotenv import dotenv_values
from modules.logging import get_logger

trues = ['true', 'yes']
falses = ['false', 'no']
int_keys = ['MAX_CONTENT_LENGTH']


def load_config(mode='', update_environ=True, working_dir=getcwd()):
    mode = environ.get('MODE', mode)

    file = f'.{mode}' if mode else ''

    file = path.join(
        working_dir if working_dir is not None else path.dirname(__file__),
        f'.env{file}'
    )
    local = f'{file}.local'

    config = {
        **dotenv_values(local if path.exists(local) else file)
    }

    for key, value in config.items():
        if value is None and environ[key] is not None:
            config[key] = environ[key]

        if update_environ:
            environ[key] = value if value is not None else environ[key]

        if value:
            if type(value) is str and value.lower() in trues:
                value = True
                config[key] = value
            elif type(value) is str and value.lower() in falses:
                value = False
                config[key] = value
            elif key.upper() in int_keys:
                value = int(value)
                config[key] = value

    get_logger('common.config').info(f'uses MODE={mode}')

    return config
