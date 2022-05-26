import re
from os import getenv, path
import pathlib
import shutil
from spex_common.services.Files import user_folder


excluded_headers = [
    'content-encoding',
    'content-length',
    'transfer-encoding',
    'connection',
    'Authorization'
]


def getFilename_fromCd(cd):

    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None

    return fname[0]


def getAbsoluteRelative(path_, absolute=True):
    if absolute:
        return path_.replace('%DATA_STORAGE%', getenv('DATA_STORAGE'))
    else:
        return path_.replace(getenv('DATA_STORAGE'), '%DATA_STORAGE%')


def download_file(path_, imgId, method='get', client=None):

    if client is None:
        return None
    dir = getenv('DATA_STORAGE') + '/' + str(imgId) + '/'
    relative_dir = '%DATA_STORAGE%' + '/' + str(imgId) + '/'
    with client.get(path_, stream=True) as r:
        filename = getFilename_fromCd(r.headers.get('content-disposition'))
        if r.ok is False:
            return None

        r.raise_for_status()
        if filename is None:
            return None
        if not path.exists(dir):
            pathlib.Path(dir).mkdir(parents=True, exist_ok=True)
        with open(dir+filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    f.close()
    return relative_dir+filename


def del_file(path_):

    _path = getAbsoluteRelative(path_, absolute=True)
    _rmDir(_path)

    return _path


def _rmDir(_path):
    shutil.rmtree(path.dirname(_path), ignore_errors=True)


def copy_file(_path, _path2='', author=None):
    _path = getAbsoluteRelative(_path, absolute=True)
    if author is not None:
        _path2 = user_folder(author)
    shutil.copyfile(_path, _path2 + path.basename(_path))
    return getAbsoluteRelative(_path2)


def _identity(item):
    return item


def first_or_none(items, transform=_identity):
    if len(items) < 1:
        return None

    transform = transform if transform is not None else _identity

    return transform(items[0]) if items[0] is not None else None


def map_or_none(items, transform=_identity):
    if len(items) < 1:
        return None

    transform = transform if transform is not None else _identity

    return [transform(item) for item in items if item is not None]
