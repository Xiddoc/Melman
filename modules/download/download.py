"""
Download a video or post from somewhere.
"""
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

from telegram.ext import ContextTypes
from yt_dlp import YoutubeDL

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp

download = MelmanModule("download", help_msg=MelmanMDHelp("""
**`download`**
Downloads video content from a link.

**Usage**
```telegram
download <LINK_TO_POST>
```
"""))


def get_download_file_prepath(temp_dir: str) -> Path:
    path_to_file = Path(temp_dir) / "vid"

    return path_to_file


def get_download_file(temp_dir: str) -> bytes:
    file, *_ = os.listdir(temp_dir)

    path_to_file = str(Path(temp_dir) / file)

    return open(path_to_file, "rb").read()


def get_youtube_config(temp_dir: str) -> Dict[str, str]:
    return {'outtmpl': str(get_download_file_prepath(temp_dir))}


# noinspection PyUnusedFunction
@download.route(re.compile(r".+"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.get_path()

    with TemporaryDirectory() as temp_dir, YoutubeDL(get_youtube_config(temp_dir)) as yt:
        yt.download(url)

        await update.message.reply_video(get_download_file(temp_dir))
