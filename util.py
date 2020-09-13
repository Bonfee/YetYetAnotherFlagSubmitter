from config import *
import os, time, subprocess
from datetime import datetime, timezone


# Returns a list of ips removing our ip from the list
def get_targets(file_path=Config.targets_file):
    # Read ips from file
    with open(file_path, 'r') as f:
        targets = f.readlines()

    # Remove blank lines
    targets = [t.strip() for t in targets if t.strip() != '']

    # Remove our ip
    if Config.team_ip in targets:
        targets.remove(Config.team_ip)
    return targets


# Returns a list of path to each exploit
def get_exploits(dir_path=Config.exploits_dir):
    return [os.path.join(dir_path, file) for file in os.listdir(dir_path) if
            os.path.isfile(os.path.join(dir_path, file))]


# Return the custom timeout for the exploit if it has one
# Otherwise it'll just return the default timeout
def get_exploit_timeout(exploit):
    # /path/to/great_exploit.py -> great_exploit
    exploit_name = os.path.splitext(os.path.basename(exploit))[0]
    try:
        return getattr(Config.Exploiter.CustomTimeouts, exploit_name)
    except AttributeError:
        return Config.Exploiter.timeout


# Gets the output returned from the gameserver
# and return the flag's status
def get_flag_status(output):
    for r in Config.Flag.Status.Returned:
        if r.value['match'] in output:
            return r.value['text']
    return 'Unknown'


# Get the current round
def get_round():
    now = datetime.now(timezone.utc).timestamp()  # Current timestamp
    start = Config.CTF.start  # CTF start timestamp
    tick = Config.CTF.tick  # Round length
    return int((now - start) / tick)


# Sleep until next round
def wait_until_next_round():
    now = datetime.now(timezone.utc).timestamp()  # Current timestamp
    start = Config.CTF.start  # CTF start timestamp
    tick = Config.CTF.tick  # Round length
    to_wait = tick - ((now - start) % tick)  # How much time till next round
    time.sleep(to_wait)


# Edit http post data - replace value 'flag' with the real  flag
def insert_flag(data, flag):
    data_ = data.copy()
    for key, value in data_.items():
        if value == 'flag':
            data_[key] = flag
            return data_
    return data_


# Installs exploits' deps
def install_exploits_deps():
    # Generate exploits/requirements.txt
    subprocess.run(['pipreqs', 'exploits/', '--force', '--no-pin', '--savepath', 'requirements-exploits.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Install requirements
    subprocess.run(['pip3', 'install', '-r', 'requirements-exploits.txt', '--user'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
