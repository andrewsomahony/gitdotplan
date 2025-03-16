import argparse
import os
import subprocess
from enum import Enum

class SupportedFile(str, Enum):
    """Enum of supported gitdotplan files."""
    PLAN = ".plan"
    """The user's current plan file."""
    PROJECT = ".project"
    """The user's current project file"""
    PROFILE = ".profile"
    """The user's current profile file"""

class InputArguments:
    """Input arguments for gitdotplan."""
    short_git_repo :str | None
    """A short version of the git repo, in the format {NAME}/{REPO_NAME}.git"""
    full_git_repo_url :str | None
    """The git repository to pull from or push to."""
    specific_file: SupportedFile | None
    """The specific file to read or edit, if any."""

    def __init__(self, short_git_repo: str | None, full_git_repo_url :str | None, specific_file: SupportedFile | None) -> None:
        """Initialize the input arguments."""
        self.short_git_repo = short_git_repo
        self.full_git_repo_url = full_git_repo_url
        self.specific_file = specific_file
        
def parse_input_arguments(default_specific_file :SupportedFile | None = None) -> InputArguments:
    """Parse the input arguments to the finger and update scripts."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="specific_file", choices=[supported_file.value for supported_file in SupportedFile], default=default_specific_file)
    git_repo_group = parser.add_mutually_exclusive_group(required=True)
    git_repo_group.add_argument("--short-repo", dest="short_repo")
    git_repo_group.add_argument("--repo", dest="git_repo")

    input_parameters = parser.parse_args()

    return InputArguments(
        input_parameters.short_repo,
        input_parameters.git_repo,
        input_parameters.specific_file
    )

def transform_short_git_repo(short_git_repo :str, writeable_required=False) -> str:
    """Transform a short repo string into a full repo URL"""
    
    ssh_url_prefix = "git@github.com:"
    https_url_prefix = "https://github.com/"

    # If writeable is required, prepend the SSH URL string, otherwise append
    # the HTTPS URL string
    return f"{ssh_url_prefix if writeable_required else https_url_prefix}{short_git_repo}"

def run_subprocess(commands: list[str], hide_output=True, cwd=None):
    """Run a subprocess in the optional working directory and potentially hide the output."""
    process = subprocess.run(
        commands,
        stdout=subprocess.DEVNULL if hide_output else None,
        stderr=subprocess.DEVNULL if hide_output else None,
        cwd=cwd
    )

    if 0 != process.returncode:
        error_message = f"Cannot run git command {' '.join(commands)}"
        raise RuntimeError(error_message)

def run_git_command(commands: list[str], cwd=None):
    """Run a git command in the optional working directory."""
    full_process = ["git"]
    full_process += commands
    # All git commands have their output hidden by default
    run_subprocess(full_process, cwd=cwd)


def clone_git_repo(repository_url, destination_directory):
    """Clones the git repo and returns the subprocess result"""
    run_git_command(
        ["clone", f"{repository_url}", f"{destination_directory}"],
    )

def get_supported_file_path(base_directory, supported_file :SupportedFile) -> str:
    return os.path.join(base_directory, supported_file)
