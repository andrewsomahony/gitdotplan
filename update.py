from os.path import exists
import tempfile
import sys
import datetime
from typing import cast

from shared import SupportedFile, clone_git_repo, get_full_git_repo_url, get_supported_file_path, parse_input_arguments, run_git_command, run_subprocess

EDITOR="nvim"

def _set_file_contents(file_path, new_contents):
    """Set the contents of the file at the given path to the new contents"""
    with open(file_path, "w") as new_file:
        new_file.write(new_contents)

if __name__ == "__main__":
    input_arguments = parse_input_arguments(SupportedFile.PLAN)
    git_repository_url = get_full_git_repo_url(input_arguments.git_repo, True)
    specific_file = cast(SupportedFile, input_arguments.specific_file)
    test_only = input_arguments.test_only

    with tempfile.TemporaryDirectory() as staging_directory:
        # Clone our gitdotplan repo
        clone_process = clone_git_repo(git_repository_url, staging_directory)

        # If we are only testing, then just see if we can write to the repo
        if test_only:
            # This command will throw an Exception if the push isn't possible,
            # even if we, as right now, are not pushing any new data
            run_git_command(["push"], cwd=staging_directory)
        else:
            # We are not testing, so perform our update

            # Get our file path
            file_path = get_supported_file_path(staging_directory, specific_file)
    
            if not exists(file_path):
                # If the file we want to edit doesn't exist, throw an error
                # This prevents someone from trying to update the wrong repo, and forces them
                # to explicitly create the needed files
                error_message = f"{specific_file} does not exist in gitdotplan repo"
                raise RuntimeError(error_message)

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


