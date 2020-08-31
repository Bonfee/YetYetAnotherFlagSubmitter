from config import *
import os


# Returns a list of ips removing our ip from the list
def get_targets(file_path=Config.targets_file):
    # Read ips from file
    with open(file_path, 'r') as f:
        targets = f.readlines()
    # Remove our ip
    if Config.team_ip in targets:
        targets.remove(Config.team_ip)

    # Remove blank lines
    targets = [t for t in targets if t.strip() != '']

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
