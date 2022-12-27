from __future__ import annotations

import pickle
import logging

from dataclasses import dataclass
from typing import List


def load_from_pickle(path: str):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        logging.error(f'Файл {path} не найден.')
        raise
    except pickle.UnpicklingError:
        logging.error(f'Файл {path} поврежден.')
        raise


@dataclass
class File:
    name: str
    decoding_table: dict
    encoded: bytes
    hash: str
    encoded_size: int


@dataclass
class Directory:
    name: str
    files: List[File]
    directories: List[Directory]


@dataclass
class Meta:
    timestamp: str
