from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class File:
    __slots__ = ["name", "decoding_table",
                 "encoded", "hash", "encoded_size"]
    name: str
    decoding_table: dict
    encoded: bytes
    hash: str
    encoded_size: int


@dataclass
class Directory:
    __slots__ = ["name", "files", "directories"]
    name: str
    files: List[File]
    directories: List[Directory]
