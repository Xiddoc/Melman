import shutil
import subprocess
import sys
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from typing import cast

from git import Repo, InvalidGitRepositoryError

from lib.commons import melman_logging
from melman import ROOT_DIR

logger = melman_logging.get_logger("MelmanUpdater")

REQUIREMENTS_FILE = "requirements.txt"
PIP_SUCCESS_CODE = 0
PIP_TIMEOUT = 120


@dataclass
class MelmanUpdater:
    git_repo: str

    def update(self) -> bool:
        """
        Updates the Melman repo in-place.

        :returns: `True` if Melman was updated.
        """
        logger.info("Checking if we should update")
        if not self._update_if_available():
            logger.info("Running latest version!")
            return False

        logger.info("Installing dependencies")
        if not self._install_requirements():
            logger.error("Could not install dependencies to update Melman.")
            return False

        logger.info("Successfully updated Melman!")
        return True

    @staticmethod
    def _install_requirements() -> bool:
        """
        Install the necessary dependencies for the project via pip.

        :returns: `True` if we managed to install the Python dependencies.
        :raises MelmanUpdateError: If we can't update the dependencies.
        """
        try:
            process = subprocess.Popen(args=[sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate(timeout=PIP_TIMEOUT)
            return process.wait(PIP_TIMEOUT) == PIP_SUCCESS_CODE
        except subprocess.CalledProcessError as exc:
            logger.info(f"Unexpected dependency installation error: {exc}")
            return False

    def _update_if_available(self) -> bool:
        """
        Returns `True` if an update was installed.
        """
        with TemporaryDirectory() as tmp:
            logger.info("Downloading remote repo")
            self._download_to(self.git_repo, tmp)
            self._move_env_to(tmp)
            remote_version = self._get_last_commit_hash(tmp)

            if self._check_for_updates(remote_version):
                logger.info(f"Newer version found, updating to: {remote_version}")
                # Delete our files to overwrite them
                shutil.rmtree(ROOT_DIR, ignore_errors=True)
                shutil.copytree(tmp, ROOT_DIR, dirs_exist_ok=True)
                return True

            return False

    def _check_for_updates(self, newer_repo_version: str) -> bool:
        """
        Returns `True` if we should go out for an update.
        """
        try:
            return self._get_last_local_commit_hash() != newer_repo_version
        except InvalidGitRepositoryError:
            return True

    @staticmethod
    def _download_to(repo_link: str, out_path: str) -> None:
        """
        Downloads the Git repo to the specified folder.
        """
        Repo.clone_from(repo_link, out_path)

    def _get_last_local_commit_hash(self) -> str:
        return self._get_last_commit_hash(".")

    @staticmethod
    def _get_last_commit_hash(repo_path: str) -> str:
        """
        :raises InvalidGitRepositoryError: If a Git repo could not be identified.
        """
        repo = Repo(path=repo_path, search_parent_directories=True)
        return cast(str, repo.head.object.hexsha)

    @staticmethod
    def _move_env_to(tmp):
        try:
            shutil.move(".env", tmp)
        except FileNotFoundError:
            logger.warning("No .env file found. This isn't an error, "
                           "but is suspicious since you should have a .env file on the disk.")
