import os
import pickle
from functools import lru_cache
import importlib.util

import numpy as np
from PIL import Image

import config

root = os.path.join(config.root, 'imgreco', 'resources')


def get_path(names):
    return os.path.join(root, *names)


def load_image(name, mode=None):
    names = name.split('/')
    path = get_path(names)
    im = Image.open(path)
    if mode is not None and im.mode != mode:
        im = im.convert(mode)
    return im


@lru_cache(maxsize=None)
def load_image_cached(name, mode=None):
    return load_image(name, mode)


def load_image_as_ndarray(name):
    return np.asarray(load_image(name))


def load_pickle(name):
    names = name.split('/')
    path = get_path(names)
    with open(path, 'rb') as f:
        result = pickle.load(f)
    return result


def load_minireco_model(name, filter_chars=None):
    model = load_pickle(name)
    if filter_chars is not None:
        model['data'] = [x for x in model['data'] if x[0] in filter_chars]
        model['chars'] = [x[0] for x in model['data']]
    return model


def get_entries(base):
    findroot = get_path(base.split('/'))
    _, dirs, files = next(os.walk(findroot))
    return (dirs, files)


spec = importlib.util.spec_from_file_location("imgreco.resources.map_vectors", os.path.join(root, 'map_vectors.py'))
map_vectors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(map_vectors)
del spec