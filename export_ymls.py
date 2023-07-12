import subprocess as sub
import re
import os
import glob
#import yaml
#modified from https://github.com/conda/conda/issues/5165

# def fix_prefix_in_yaml_files(directory):
#     # List all files in the directory
#     files = os.listdir(directory)
#
#     for file_name in files:
#         if file_name.endswith('.yml') or file_name.endswith('.yaml'):
#             file_path = os.path.join(directory, file_name)
#
#             with open(file_path, 'r') as file:
#                 # Load the YAML content
#                 data = yaml.safe_load(file)
#                 # Fix the prefix value
#                 if 'prefix' in data:
#                     data['prefix'] = data['prefix'].strip()
#                 # Save the updated YAML content
#                 with open(file_path, 'w') as file:
#                     yaml.dump(data, file)


def export_ymls():

    # create list of current environments
    sub.check_call(" ".join(['conda','env','list','>','envs.txt']),shell=True)

    # load and parse environment names
    envs = {}
    with open("envs.txt", 'r') as f:
        lines = f.read().splitlines()
        lines = [l.replace("*", "") for l in lines]  # get rid of asterisk which denotes active environment
        for line in lines[2:]:
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

    # write environment packages out

    #change to your preferred directory location
    directory = os.getcwd()

    os.chdir(directory)
    for env_name, directory in envs.items():
        print("Backing up...",env_name)


        if "_not_in_default_path" in env_name:
            cmd = f"conda env export --no-build --p {directory} > {env_name}.yml"
        else:
            cmd = f"conda env export --no-build --name {env_name} > {env_name}.yml"


        sub.check_call(cmd,shell=True)

    # directory = 'C:/Users/' + os.getlogin() + '/OneDrive - James Cook University/Postgraduate/conda_yml'
    # fix_prefix_in_yaml_files(directory)

if __name__ == '__main__':
    export_ymls()