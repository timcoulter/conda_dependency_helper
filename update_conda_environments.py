import os
import subprocess
import re
from export_conda_dependencies import export_env_dependencies
from configure_conda import configure_conda_envs
import time

def create_or_update_environment(env_name, yml_file):
    # Check if the environment already exists
    env_exists = subprocess.call(f"conda activate {env_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

    if env_exists:
        # Update the existing environment
        print(f"Updating existing environment: {env_name}")
        subprocess.check_call(f"conda env update --name {env_name} --file \"{yml_file}\" --prune", shell=True)

    else:
        # Create a new environment
        print(f"Creating new environment: {env_name}")
        subprocess.check_call(f"conda env create --name {env_name} --file \"{yml_file}\"", shell=True)
        subprocess.check_call(f"conda install --name {env_name} pip --yes")

if __name__ == '__main__':
    configure_conda_envs()

    env_dependency_folder = os.path.join(os.getcwd(),'env_dependencies')
    if not os.path.exists(env_dependency_folder):
        print("No conda environment dependencies found at: {0}".format(env_dependency_folder))
    else:

        # Start the timer
        start_time = time.time()

        # Iterate over the .yml files in the folder
        for file in os.listdir(env_dependency_folder):
            if file.endswith(".yml"):
                env_name = os.path.splitext(file)[0]
                yml_file = os.path.join(env_dependency_folder, file)
                create_or_update_environment(env_name, yml_file)

        # Stop the timer
        elapsed_time = time.time() - start_time
         # Print the elapsed time
        print(f"\nSerial processing completed in {elapsed_time:.2f} seconds\n")


    export_env_dependencies()
