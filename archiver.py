from __future__ import annotations

import hashlib
import pickle
import os

from typing import Optional

import shannon_fano

from file_models import File, Directory, MetaWrapper, load_from_pickle
from file_system import get_directory, get_files


def decode_file(file: File, output_path: Optional[str] = None) -> None:
    encoded = ''.join([bin(byte)[2:].zfill(8) for byte in file.encoded])
    last = encoded[-8:]
    last = last[-(file.encoded_size % 8):]
    encoded = encoded[:-8] + last
    decoded_bytes = shannon_fano.decode(encoded, file.decoding_table)

    path = (file.name if output_path is None
            else f'{output_path}/{file.name}')

    try:
        with open(path, 'wb') as f:
            f.write(decoded_bytes)
    except FileNotFoundError:
        raise

    if hashlib.md5(decoded_bytes).hexdigest() != file.hash:
        raise OSError(f'Файл {file.name} поврежден.')


class Decoder:
    def __init__(
            self,
            input_path: str,
            output_path: Optional[str] = None
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.meta = load_from_pickle(input_path)
        self.archived_data = self.meta.file_model

    def decode(self) -> None:
        if self.meta.password_hash:
            password = input('Введите пароль: ')
            if (hashlib.sha256(password.encode()).hexdigest()
                    != self.meta.password_hash):
                raise ValueError('Неверный пароль.')

        if isinstance(self.archived_data, list):
            self._decode_files()
        else:
            self._decode_directory()

    def _decode_files(self) -> None:
        for file in self.archived_data:
            decode_file(file, self.output_path)

    def _decode_directory(
            self,
            directory: Optional[Directory] = None,
            path: Optional[str] = None) -> None:
        if path is None:
            path = f'{self.output_path}/{self.archived_data.name}'

        if directory is None:
            directory = self.archived_data

        if not os.path.exists(path):
            os.mkdir(path)

        for file in directory.files:
            decode_file(file, path)

        for dir in directory.directories:
            self._decode_directory(dir, f'{path}/{dir.name}')

    @property
    def file_listings(self) -> str:
        if isinstance(self.archived_data, list):
            return '\n'.join([file.name for file in self.meta.file_model])
        else:
            return str(self.archived_data)


class Encoder:
    def __init__(self, *input_paths: str,
                 output_path: Optional[str] = None,
                 password: Optional[str] = None) -> None:
        if os.path.isdir(input_paths[0]):
            self.model = get_directory(input_paths[0])
        else:
            self.model = get_files(*input_paths)

        self.model = MetaWrapper(self.model, password)
        self.output_path = (f'{self.model.name}.sf' if not output_path
                            else f'{output_path}/{self.model.name}.sf')

    def encode(self) -> None:
        with open(self.output_path, 'wb') as f:
            f.write(pickle.dumps(self.model))
