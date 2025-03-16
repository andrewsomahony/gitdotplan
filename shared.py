import argparse
import os
import subprocess
import re
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
    git_repo :str
    """The git repository to pull from or push to."""
    specific_file: SupportedFile | None
    """The specific file to read or edit, if any."""
    test_only: bool
    """Whether to just test the functionality."""

    def __init__(self, git_repo :str, specific_file: SupportedFile | None, test_only: bool) -> None:
        """Initialize the input arguments."""
        self.git_repo = git_repo
        self.specific_file = specific_file
        self.test_only = test_only
        
def parse_input_arguments(default_specific_file :SupportedFile | None = None) -> InputArguments:
    """Parse the input arguments to the finger and update scripts."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="specific_file", choices=[supported_file.value for supported_file in SupportedFile], default=default_specific_file)
    parser.add_argument("--repo", required=True, dest="git_repo")
    parser.add_argument("--test-only", action="store_true", dest="test_only")

    input_parameters = parser.parse_args()

    return InputArguments(
        input_parameters.git_repo,
        input_parameters.specific_file,
        input_parameters.test_only
    )

def get_full_git_repo_url(git_repo :str, writeable_required: bool) -> str:
    """Transforms the input repo into a full URL."""
    git_extension_regex_pattern = r"([~@\:\._\-\w\/]+)\.git$"
    git_ssh_url_regex_pattern = r"^git@github\.com:([~@\:\._\-\w\/]+)\.git$"
    git_https_url_regex_pattern = r"^https:\/\/(?:www\.)?github\.com\/([~@\:\._\-\w\/]+)\.git$"

    # We first want to see if we have the git extension at all, and if so, then we can
    # check our full URL.  If not, we just have to use the URL as-is and assume that it's
    # a raw IP address or something

    if re.match(git_extension_regex_pattern, git_repo):
        # We have a git extension, so now see if our input repo string matches the SSH or
        # HTTPS patterns.  If they do, return them as-is, otherwise generate one
        if re.match(git_ssh_url_regex_pattern, git_repo) or \
            re.match(git_https_url_regex_pattern, git_repo):
            return git_repo
        else:
            # We need to generate a repo, so do so based on our writeable_required URL
            ssh_url_prefix = "git@github.com:"
            https_url_prefix = "https://github.com/"
        
            # If writeable is required, prepend the SSH URL string, otherwise append
            # the HTTPS URL string
            return f"{ssh_url_prefix if writeable_required else https_url_prefix}{git_repo}"
            
    else:
        # We have a URL of some kind without the git extension, so return it as-is
        return git_repo

def run_subprocess(commands: list[str], hide_output=True, cwd=None):
    """Run a subprocess in the optional working directory and potentially hide the output."""
    process = subprocess.run(
        commands,
        stdout=subprocess.DEVNULL if hide_output else None,
        stderr=subprocess.DEVNULL if hide_output else None,
        cwd=cwd
    )

    if 0 != process.returncode:
        error_message = f"Error in subprocess: {' '.join(commands)}"
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
