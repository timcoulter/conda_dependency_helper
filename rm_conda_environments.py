import subprocess
import re


def remove_conda_environments():
    # Get output of "conda env list" command
    env_list_output = subprocess.Popen(['conda', 'env', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]

    # Fix some problems in env txt
    env_list_output = env_list_output.replace('[0m[0m', '')
    env_list_output = env_list_output.replace('[0m', '')

    # Load and parse environment names
    envs = {}
    lines = env_list_output.splitlines()
    lines = [l.replace("*", "") for l in lines[2:]]  # Get rid of asterisk which denotes active environment
    for line in lines:
        line_match = re.findall(r'(\w*)\s+(C:.*)', line)
        if line_match:
            name, directory = line_match[0]
            if not name:
                local_name = directory.split("\\")[-1]
                print(f"Environment {local_name} is not installed in the default conda environment directory.")
                print(f"The environment name will be appended with '_not_in_default_path'")
                envs[f"{local_name}_not_in_default_path"] = directory
            else:
                envs[name] = directory

    # Remove each environment
    for environment, directory in envs.items():
        if environment == 'base':
            continue
        print(f"Removing environment: {environment}")
        try:
            subprocess.check_output(['conda', 'remove', '--name', environment,'--all','--yes'], universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print(f"Error removing environment {environment}: {e}")

    print("All conda environments have been removed.")


if __name__ == '__main__':
    remove_conda_environments()
