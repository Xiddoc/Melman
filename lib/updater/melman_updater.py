import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from tempfile import TemporaryDirectory

import requests
from git import Repo, InvalidGitRepositoryError

from lib import melman_logging
from lib.melman_errors import MelmanUpdateError
from melman import ROOT_DIR

logger = melman_logging.get_logger("MelmanUpdater")

GIT_SUFFIX = '.git'
LAST_HASH_REGEX = re.compile(r'"/.*?/.*?/commit/([\w\d]*?)"')
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
              "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
REQUIREMENTS_FILE = "requirements.txt"


@dataclass
class MelmanUpdater:
    git_repo: str

    def update(self) -> bool:
        """
        Updates the Melman repo in-place.

        :returns: `True` if Melman was updated.
        """
        logger.info("Checking if we should update...")
        if False and not self._check_for_updates():  # TODO REMOVE FALSE
            logger.info("Running the latest version!")
            return False

        logger.info("Updating Melman...")
        self._download_to_project()

        logger.info("Installing dependencies...")
        try:
            self._install_requirements()
        except MelmanUpdateError:
            logger.error("Could not install dependencies to update Melman.")
            return False

        return True

    @staticmethod
    def _install_requirements() -> None:
        """
        Install the necessary dependencies for the project via pip.

        :raises MelmanUpdateError: If we can't update the dependencies.
        """
        try:
            subprocess.check_call(args=[sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as exc:
            raise MelmanUpdateError("Can't install dependencies due to pip error.") from exc

    def _download_to_project(self) -> None:
        with TemporaryDirectory() as tmp:
            self._download_to(self.git_repo, tmp)
            shutil.copytree(tmp, ROOT_DIR, dirs_exist_ok=True)

    def _check_for_updates(self) -> bool:
        """
        Returns `True` if we should go out for an update.
        """
        try:
            return self._get_last_local_commit_hash() != self._get_last_remote_commit_hash(self.git_repo)
        except InvalidGitRepositoryError:
            return True

    @staticmethod
    def _download_to(repo_link: str, out_path: str) -> None:
        """
        Downloads the Git repo to the specified folder.
        """
        Repo.clone_from(repo_link, out_path)

    @staticmethod
    def _get_last_remote_commit_hash(repo_link: str) -> str:
        front_page = requests.get(url=repo_link.removesuffix(GIT_SUFFIX),
                                  headers=DEFAULT_HEADERS)

        if front_page.status_code != 200:
            raise MelmanUpdateError("Git repo does not seem reachable.")

        hash_match = LAST_HASH_REGEX.search(front_page.text)

        if hash_match is None:
            raise MelmanUpdateError("Could not identify most recent hash in Git repo.")

        return hash_match.group(1)

    @staticmethod
    def _get_last_local_commit_hash() -> str:
        """
        :raises InvalidGitRepositoryError: If a Git repo could not be identified.
        """
        repo = Repo(search_parent_directories=True)
        return repo.head.object.hexsha
