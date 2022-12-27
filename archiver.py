import hashlib
import logging
import pickle
import os
from dataclasses import dataclass

from shannon_fano import ShannonFano


@dataclass
class File:
    name: str
    decoding_table: dict
    encoded: bytes
    hash: str


class Archiver:
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

    def __get_file(self) -> File:
        encoded = self.shannon_fano.encode()
        encoded_bytes = bytes()
        for i in range(0, len(encoded), 8):
            encoded_bytes += int(encoded[i:i + 8], 2).to_bytes(1, 'big')
        return File(name=self.name,
                    decoding_table=self.shannon_fano.codes,
                    encoded=encoded_bytes,
                    hash=self.hash)

    def encode(self, output_path: str = None) -> None:
        file = self.__get_file()

        path = f'{file.name}.sf' if output_path is None \
            else f'{output_path}/{file.name}.sf'
        with open(path, 'wb') as f:
            f.write(pickle.dumps(file))
        encoded_file_size = os.path.getsize(path)
        logging.info('Запись в архив завершена.')
        logging.info(f'Размер файла до сжатия {self.file_size} bytes')
        logging.info(f'Размер файла после сжатия {encoded_file_size} bytes')
        logging.info(f'Процент сжатия составил '
                     f'{100 * (1 - encoded_file_size // self.file_size)}%')
        logging.info(f'Конечный путь: {path}')

    @staticmethod
    def __load_file(path: str) -> File:
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            logging.error(f'Файл {path} не найден.')
            raise FileNotFoundError
        except pickle.UnpicklingError:
            logging.error(f'Файл {path} поврежден.')
            raise pickle.UnpicklingError

    @staticmethod
    def decode(input_path: str, output_path: str = None) -> None:
        file = Archiver.__load_file(input_path)
        encoded = ''.join([bin(byte)[2:].zfill(8) for byte in file.encoded])
        decoded_bytes = ShannonFano.decode(encoded, file.decoding_table)

        path = file.name if output_path is None \
            else f'{output_path}/{file.name}'

        try:
            with open(path, 'wb') as f:
                f.write(decoded_bytes)
        except FileNotFoundError:
            logging.error(f'Путь {output_path} не найден.')
            raise FileNotFoundError

        logging.info('Распаковка завершена.')
        logging.info(f'Конечный путь: {path}')

        if hashlib.md5(decoded_bytes).hexdigest() != file.hash:
            logging.warning('Файл поврежден.')


if __name__ == '__main__':
    # archiver = Archiver('ArseniyFrog.png')
    # archiver.encode()
    Archiver.decode('ArseniyFrog.png.sf', 'decoded')
