import os

from file_models import File, Directory, List


def get_directory(path: str) -> Directory:
    root_dir = Directory(path.split('/')[-1], [], [])
    for root, dirs, files in os.walk(path):
        for file in files:
            root_dir.files.append(get_file(f'{root}/{file}'))
        for directory in dirs:
            root_dir.directories.append(get_directory(f'{root}/{directory}'))
    return root_dir


def get_files(*paths: str) -> List:
    try:
        return [get_file(path) for path in paths]
    except FileNotFoundError:
        raise FileNotFoundError


def get_file(path: str) -> File:
    return File.from_file(path)
