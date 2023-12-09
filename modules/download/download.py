"""
Download a video or post from somewhere.
"""
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Any

from telegram.ext import ContextTypes
from yt_dlp import YoutubeDL # type: ignore

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp, melman_logging

OUT_PATH_SUFFIX = '_OUT.mp4'
BITRATE = '500k'

download = MelmanModule("download", help_msg=MelmanMDHelp("""
**`download`**
Downloads video content from a link.

**Usage**
```telegram
download <LINK_TO_POST>
```
"""))

logger = melman_logging.get_logger("Downloader")


def get_download_file_prepath(temp_dir: str) -> Path:
    path_to_file = Path(temp_dir) / "vid"

    return path_to_file


def get_output_file_path(temp_dir: str, suffix: str = "") -> str:
    file, *_ = os.listdir(temp_dir)

    path_to_file = str(Path(temp_dir) / (file + suffix))

    return path_to_file


def get_download_file(temp_dir: str) -> bytes:
    return open(get_output_file_path(temp_dir), "rb").read()


def get_youtube_config(temp_dir: str) -> Dict[str, Any]:
    return {'outtmpl': str(get_download_file_prepath(temp_dir)), "quiet": True}


# noinspection PyUnusedFunction
@download.route(re.compile(r".+"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.get_path()

    with TemporaryDirectory() as temp_dir, YoutubeDL(get_youtube_config(temp_dir)) as yt:
        logger.info(f"Downloading video: '{url}'")
        yt.download(url)

        logger.info(f"Compressing video: '{url}'")
        os.system(f'ffmpeg -i "{get_output_file_path(temp_dir)}" '
                  f'-b {BITRATE} '
                  f'"{get_output_file_path(temp_dir, suffix=OUT_PATH_SUFFIX)}"')

        logger.info(f"Sending video: '{url}'")
        await update.message.reply_video(get_download_file(temp_dir))
