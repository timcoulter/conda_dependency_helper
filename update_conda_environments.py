import os
import subprocess
import re
from export_ymls import export_env_dependencies
from configure_conda import configure_conda_envs

def create_or_update_environment(env_name, yml_file, pip_file=None):
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
        subprocess.check_call(f"conda install --name {env_name} -c conda-forge pip-tools --yes")

    if pip_file:
        # Install pip packages from the provided text file
        print(f"Installing pip packages for environment: {env_name}")
        #subprocess.check_call(f"conda run --name {env_name} pip install --upgrade --requirement \"{pip_file}\"",
        #                      shell=True)
        subprocess.check_call(f"conda run --name {env_name} pip-sync \"{pip_file}\"",shell=True)


if __name__ == '__main__':
    configure_conda_envs()

    env_dependency_folder = os.path.join(os.getcwd(),'env_dependencies')
    if not os.path.exists(env_dependency_folder):
        print("No conda environment dependencies found at: {0}".format(env_dependency_folder))
    else:
        # Iterate over the .yml files in the folder
        for file in os.listdir(env_dependency_folder):
            if file.endswith(".yml"):
                env_name = os.path.splitext(file)[0]
                yml_file = os.path.join(env_dependency_folder, file)
                pip_file = os.path.join(env_dependency_folder, f"{env_name}.txt")
                if os.path.isfile(pip_file):
                    create_or_update_environment(env_name, yml_file, pip_file)
                else:
                    create_or_update_environment(env_name, yml_file)

    export_env_dependencies()
