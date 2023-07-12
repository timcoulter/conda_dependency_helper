import os
import subprocess
import yaml
from export_ymls import export_ymls

def fix_yml_prefix(yml_file):
    # Load the YAML file
    with open(yml_file, "r") as file:
        data = yaml.safe_load(file)

    old_path = data['prefix']
    fixed_path = old_path.replace('\\', '/')
    # Split the path into directory parts
    parts = fixed_path.split('/')
    # Find the index of the 'Users' directory
    users_index = parts.index('Users')
    # Update the username
    parts[users_index + 1] = os.getlogin()
    # Join the parts back into a new path
    new_path = '/'.join(parts)
    data['prefix'] = new_path

    # Write the modified YAML back to the file
    with open(yml_file, "w") as file:
        yaml.dump(data, file)

def create_or_update_environment(env_name, yml_file):

    #make prefix of yml the same as the user
    fix_yml_prefix(yml_file)

    env_exists = subprocess.call(f"conda activate {env_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

    if env_exists:
        print(f"Updating environment '{env_name}' using {yml_file}...")
        subprocess.call(f"conda env update --name {env_name} --file \"{yml_file}\"", shell=True)
    else:
        print(f"Creating environment '{env_name}' using {yml_file}...")
        subprocess.call(f"conda env create --name {env_name} --file \"{yml_file}\"", shell=True)

if __name__ == '__main__':
    # Folder path containing the .yml files
    yml_folder = os.getcwd()

    # Activate the base Conda environment
    subprocess.call("conda activate base", shell=True)

    # Update conda
    print("Updating base conda")
    subprocess.call("conda update -n base conda --yes", shell=True)
    #print install pip
    subprocess.call("conda install pip --yes", shell=True)
    #ensure pyyaml is installed
    subprocess.call("conda install pyyaml  --yes", shell=True)
    # Ensure better solver is installed and configured
    print("Installing better conda environment solver")
    subprocess.call("conda install -n base conda-libmamba-solver --yes", shell=True)
    subprocess.call("conda config --set solver libmamba", shell=True)

    # Iterate over the .yml files in the folder
    for file in os.listdir(yml_folder):
        if file.endswith(".yml"):
            env_name = os.path.splitext(file)[0]
            yml_file = os.path.join(yml_folder, file)
            create_or_update_environment(env_name, yml_file)

    export_ymls()
