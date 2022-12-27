import os
import logging
import hashlib

from shannon_fano import ShannonFano
from file_models import File, Directory, List


def get_directory(path: str) -> Directory:
    root_dir = Directory(path.split('/')[-1], [], [])
    for root, dirs, files in os.walk(path):
        for file in files:
            root_dir.files.append(get_file(f'{root}/{file}'))
        for directory in dirs:
            root_dir.directories.append(get_directory(f'{root}/{directory}'))
    return root_dir


def get_files(*paths: str) -> List[File]:
    try:
        return [get_file(path) for path in paths]
    except FileNotFoundError:
        logging.error('Файл не найден.')
        raise FileNotFoundError


def get_file(path: str) -> File:
    return FileSerializer(path).file


class FileSerializer:
    def __init__(self, path: str) -> None:
        self.name = os.path.basename(path)
        self.file_size = os.path.getsize(path)

        try:
            with open(path, 'rb') as file:
                self.bytes = file.read()
        except FileNotFoundError:
            logging.error(f'Файл {path} не найден.')
            raise FileNotFoundError

        self.hash = hashlib.md5(self.bytes).hexdigest()

        self.shannon_fano = ShannonFano(self.bytes)

    @property
    def file(self) -> File:
        encoded = self.shannon_fano.encode()
        encoded_bytes = bytes()
        for i in range(0, len(encoded), 8):
            encoded_bytes += int(encoded[i:i + 8], 2).to_bytes(1, 'big')
        return File(name=self.name,
                    decoding_table=self.shannon_fano.codes,
                    encoded=encoded_bytes,
                    hash=self.hash,
                    encoded_size=len(encoded))
