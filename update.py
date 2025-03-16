from os.path import exists
import tempfile
import sys
import datetime
from typing import cast

from shared import SupportedFile, clone_git_repo, get_supported_file_path, parse_input_arguments, run_git_command, run_subprocess, transform_short_git_repo

EDITOR="nvim"

def _set_file_contents(file_path, new_contents):
    """Set the contents of the file at the given path to the new contents"""
    with open(file_path, "w") as new_file:
        new_file.write(new_contents)

if __name__ == "__main__":
    input_arguments = parse_input_arguments(SupportedFile.PLAN)
    git_repository_url = transform_short_git_repo(str(input_arguments.short_git_repo), True) \
                            if None is not input_arguments.short_git_repo else input_arguments.full_git_repo_url

    with tempfile.TemporaryDirectory() as staging_directory:
        specific_file=cast(SupportedFile, input_arguments.specific_file)

        # Clone our gitdotplan repo
        clone_process = clone_git_repo(git_repository_url, staging_directory)

        # Get our file path
        file_path = get_supported_file_path(staging_directory, specific_file)

        if not exists(file_path):
            # If we don't have the file in our directory, just create one
            with open(file_path, "w"):
                pass
        
        # We can get input from stdin, which will represent the new contents of our file,
        # or we can call our editor manually.  If we don't have anything in stdin, we will
        # call our editor to obtain our text

        # The idea behind stdin is that we want to make an editor plugin to accept the new data
        # someday, while the editor call itself is temporary just so we can edit now without much
        # hassle

        if not sys.stdin.isatty():
            file_data = sys.stdin.read()
        else:
            # Run our editor process; this method will throw an Exception if the process exits
            # with a non-zero return code
            run_subprocess(
                [EDITOR, file_path],
                hide_output=False,
                cwd=staging_directory
            )

            # We have made our edit in our editor, so obtain our file_data from the file
            # itself
            with open(file_path) as new_file:
                file_data = new_file.read()

        # Set our file contents with our file data
        _set_file_contents(
            file_path,
            file_data
        )
        # We have made our edit, now we can commit and push

        # Create our commit message with the date and time of the update
        commit_message = f"{specific_file} file update {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        # Commit our new file
        run_git_command(
            ["commit", "-a", f"-m{commit_message}"],
            cwd=staging_directory
        )

        # Push our change up to our remote gitdotplan repo
        run_git_command(
            ["push"],
            cwd=staging_directory
        )


