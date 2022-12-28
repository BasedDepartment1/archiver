from __future__ import annotations

import pickle
import logging

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import List, Optional


def load_from_pickle(path: str) -> MetaWrapper:
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

    def __str__(self):
        return self.get_recursive_listing()

    def get_recursive_listing(self, level=0):
        result = f'{"  " * level}└{self.name}\n'
        for file in self.files:
            result += f'{"  " * (level + 1)}{file.name}\n'
        for directory in self.directories:
            result += directory.get_recursive_listing(level + 1)
        return result


class MetaWrapper:
    def __init__(self, model, password: Optional[str] = None):
        self.file_model = model
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.name = self._get_name()
        self.password_hash = (sha256(password.encode()).hexdigest()
                              if password else None)

    def _get_name(self):
        if isinstance(self.file_model, list):
            return self.file_model[0].name
        return self.file_model.name
