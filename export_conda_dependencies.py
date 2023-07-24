import subprocess as sub
import re
import os
from configure_conda import configure_conda_envs

def remove_ansi_escape_sequences(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace('[0m[0m', '')
    content = content.replace('[0m', '')

    with open(file_path, 'w') as file:
        file.write(content)

def remove_ansi_escape_sequences_recursive(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.txt', '.yml')):
                file_path = os.path.join(root, file)
                remove_ansi_escape_sequences(file_path)

def export_env_dependencies():

    # Get output of "conda env list" command
    env_list_output = sub.Popen(['conda', 'env', 'list'], stdout=sub.PIPE, stderr=sub.PIPE, text=True).communicate()[0]

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

    # Create env_dependencies folder if it doesn't exist
    folder_name = "env_dependencies"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Write environment packages out
    current_directory = os.getcwd()
    for env_name, directory in envs.items():
        print("Backing up...", env_name)
        output_folder = os.path.join(current_directory, folder_name)

        if "_not_in_default_path" in env_name:
            conda_cmd = f"conda env export --no-build --p {directory} > {env_name}.yml"
        else:
            conda_cmd = f"conda env export --no-build --name {env_name} > {env_name}.yml"

        os.chdir(output_folder)
        sub.check_call(conda_cmd, shell=True)

    remove_ansi_escape_sequences_recursive(output_folder)

if __name__ == '__main__':
    export_env_dependencies()
