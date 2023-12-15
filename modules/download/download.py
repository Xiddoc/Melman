"""
Download a video or post from somewhere.
"""
import os
import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Any

from telegram.ext import ContextTypes
from yt_dlp import YoutubeDL  # type: ignore
from yt_dlp.utils import DownloadError  # type: ignore

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp
from lib.commons import melman_logging

OUT_PATH_SUFFIX = '_OUT.mp4'
BITRATE = '500k'
COMPRESS_TIMEOUT = 60 * 3

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


def get_youtube_config(temp_dir: str) -> Dict[str, Any]:
    return {
        'outtmpl': str(get_download_file_prepath(temp_dir)),
        "quiet": True,
        "no_warnings": True,
        "format": "worst"
    }


def compress_video(input_file: str, output_file: str) -> None:
    process = subprocess.Popen(['ffmpeg', '-i', input_file, '-b', BITRATE, output_file],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.communicate()
    process.wait(COMPRESS_TIMEOUT)


def convert_video_to_mp3(input_file: str) -> str:
    output_file = input_file + '.mp3'

    process = subprocess.Popen(['ffmpeg', '-i', input_file, output_file],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.communicate()
    process.wait(COMPRESS_TIMEOUT)

    return output_file


async def _unsafe_download_media(url: str, convert_to_mp3: bool = False) -> bytes:
    """
    :raises DownloadError: If YT-DLP fails to download the video.
    :raises TimeoutExpired: If FFMPEG took too long to compress the video.
    :raises OSError: The `open` command fails while trying to get the file- FFMPEG didn't succeed at compressing.
    """
    with TemporaryDirectory() as temp_dir, YoutubeDL(get_youtube_config(temp_dir)) as yt:
        logger.info(f"Downloading video: '{url}'")
        yt.download(url)

        logger.info(f"Compressing video: '{url}'")
        input_video = get_output_file_path(temp_dir)
        output_video = input_video + OUT_PATH_SUFFIX
        compress_video(input_video, output_video)

        if convert_to_mp3:
            logger.info(f"Converting to MP3: '{url}'")
            output_video = convert_video_to_mp3(output_video)

        return open(output_video, "rb").read()


# noinspection PyUnusedFunction
@download.route(re.compile(r"^(?!mp3).+"))
async def download_video(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.get_path()

    try:
        file = await _unsafe_download_media(url)

        logger.info(f"Sending video: '{url}'")
        await update.message.reply_video(file)
    except DownloadError as exc:
        logger.error(f"Couldn't download video '{url}': {exc}")
        await update.message.reply_text("Error encountered while downloading the video, "
                                        "failed with error: " + str(exc))
    except (subprocess.TimeoutExpired, OSError) as exc:
        logger.error(f"Timeout expired or error while compressing '{url}': {exc}")
        await update.message.reply_text("Error encountered while compressing the video. "
                                        "Try again with a shorter video?")


# noinspection PyUnusedFunction
@download.route(re.compile(r"mp3 .+"))
async def download_music(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.get_path().removeprefix('mp3 ')

    try:
        await update.message.reply_text("Processing...")
        file = await _unsafe_download_media(url, convert_to_mp3=True)

        logger.info(f"Sending audio: '{url}'")
        await update.message.reply_audio(file)
    except DownloadError as exc:
        logger.error(f"Couldn't download video '{url}': {exc}")
        await update.message.reply_text("Error encountered while downloading the video, "
                                        "failed with error: " + str(exc))
    except (subprocess.TimeoutExpired, OSError) as exc:
        logger.error(f"Timeout expired or error while processing '{url}': {exc}")
        await update.message.reply_text("Error encountered while processing the video. "
                                        "Try again with a shorter clip?")
