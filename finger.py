from os.path import exists
import tempfile
from typing import cast

from shared import SupportedFile, clone_git_repo, get_full_git_repo_url, get_supported_file_path, parse_input_arguments

if __name__ == "__main__":
    input_arguments = parse_input_arguments()
    # Set our repository URL
    git_repository_url = get_full_git_repo_url(input_arguments.git_repo, True)

    # Create a temporary directory to store our files
    with tempfile.TemporaryDirectory() as staging_directory:
        # Clone our gitdotplan repo
        clone_git_repo(git_repository_url, staging_directory)

        if None is input_arguments.specific_file:
            # If we don't have a specific file to read, then just read and format
            # our standard fingerserver files, which are .plan, .project, and .profile

            # Obtain our relevant file paths
            profile_file_path = get_supported_file_path(staging_directory, SupportedFile.PROFILE)
            project_file_path = get_supported_file_path(staging_directory, SupportedFile.PROJECT)
            plan_file_path = get_supported_file_path(staging_directory, SupportedFile.PLAN)
    
            # Read our files in the specific order, add some formatting,
            # and output to stdout
    
            if exists(profile_file_path):
                with open(profile_file_path, "r") as profile_fd:
                    print("Profile")
                    print("-------")
                    print(profile_fd.read())
                    # Print an extra newline for spacing
                    print("")
            else:
                print("No profile information")
            
            if exists(project_file_path):
                with open(project_file_path, "r") as project_fd:
                    print("Current Project(s)")
                    print("------------------")
                    print(project_fd.read())
                    # Print an extra newline for spacing
                    print("")
            else:
                print("No Current Projects")
                
            if exists(plan_file_path):
                with open(plan_file_path, "r") as plan_fd:
                    print(".plan file")
                    print("----------")
                    print(plan_fd.read())
                    # Print an extra newline for spacing
                    print("")
            else:
                print("No .plan")
        else:
            # Read the specific file and output its contents.
            # If the file doesn't exist, nothing is output

            # Get the supported file path
            file_path = get_supported_file_path(staging_directory, cast(SupportedFile, input_arguments.specific_file))

            # If the file exists, then read it and output its contents to stdout
            if exists(file_path):
                with open(file_path, "r") as fd:
                    print(fd.read())
