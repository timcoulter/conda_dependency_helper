import subprocess as sub
import re
import os

def find_last_true(bool_list):
    for i in range(len(bool_list) - 1, -1, -1):
        if bool_list[i] == True:
            return i
    return -1  # Return -1 if no `True` value is found

def fix_envs_txt():
    lines = []
    with open('envs.txt', 'r') as file:
        lines = file.readlines()
    
    regex_pattern = r"([a-zA-Z]:\\[^<>:\"/\\|?*\n]+(\\[^<>:\"/\\|?*\n]+)*\\?|^\\\\[^<>:\"/\\|?*\n]+(\\[^<>:\"/\\|?*\n]+)*\\?)"
    
    #find if the line contains a file path format.
    path_in_line = []
    for l in lines:
        matches = re.findall(regex_pattern, l)
        path_in_line.append(bool(matches))

    #crop bool list so the last item is true, while keeping all trues
    last_true_idx = find_last_true(path_in_line)

    #make lines the same length as path_in_line
    lines = lines[:(last_true_idx+1)]

    #write new lines to file, also removing old ones
    with open('envs.txt', 'w') as file:
        pass  # Open the file and immediately close it to clear its contents
    with open('envs.txt', 'a') as file:
        file.writelines(lines)

def export_ymls():

    # create list of current environments
    sub.check_call(" ".join(['conda','env','list','>','envs.txt']),shell=True)

    #fix some problems in env txt
    fix_envs_txt()

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