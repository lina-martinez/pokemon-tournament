from dataclasses import dataclass
from typing import Sequence

import numpy as np
import requests


@dataclass
class DownloadableCharacter:
    name: str
    url: str


class ImageRepository:
    def __init__(self, characters: Sequence[DownloadableCharacter]) -> None:
        self._characters = characters

    def retrieve(self, name: str) -> np.ndarray:
        with requests.Session() as session:
            downloadable = list(filter(lambda download: download.name == name, self._characters))[0]
            return download_img(session, downloadable.url)


def download_img(session, sprite_url: str):
    content = None
    with session.get(sprite_url) as response:
        if response.status_code == 200:
            content = response.content
    return content
