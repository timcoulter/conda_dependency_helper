import subprocess

def configure_conda_envs():
    # Activate the base Conda environment
    subprocess.call("conda activate base", shell=True)

    #configuring conda package channel
    subprocess.call("conda config --set channel_priority flexible", shell=True)
    subprocess.call("conda config --remove-key channels", shell=True)
    subprocess.call("conda config --add channels conda-forge", shell=True)
    subprocess.call("conda config --add channels defaults", shell=True)
    subprocess.call("conda config --set pip_interop_enabled False", shell=True)
    subprocess.call("conda config --set report_errors false",shell=True)

    # Update conda
    print("Updating base conda")
    subprocess.call("conda update -n base conda --yes", shell=True)

    # Ensure better solver is installed and configured
    print("Installing better conda environment solver")
    subprocess.call("conda install -n base conda-libmamba-solver --yes", shell=True)
    subprocess.call("conda config --set solver libmamba", shell=True)


    # install pip and pip-sync to all conda environments on the system
    print("Installing pip to all conda environments on the system")
    subprocess.check_call("conda install --all pip --yes", shell=True)


    conda_doctor()
    #clean conda 
    subprocess.call("conda clean --all --yes", shell=True)

def conda_doctor():
    # Get a list of all Conda environments
    process = subprocess.Popen(['conda', 'env', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    environments = [line.split()[0] for line in output.decode().splitlines() if not line.startswith('#') and line.strip()]

    # Loop through each environment
    for env in environments:
        print(f"Running conda doctor for environment: {env}")

        # Activate the environment
        activate_cmd = f"conda doctor --name {env}"
        subprocess.run(activate_cmd, shell=True)

if __name__ == '__main__':
    configure_conda_envs()
