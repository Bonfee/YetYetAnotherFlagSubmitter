from config import *
import os
import socket
import urllib.parse


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


# Alternative method to send flags to the local API using socket instead of requests library
def store_flag(flag, exploit, target):
    data = urllib.parse.urlencode({'flag': flag, 'exploit': exploit, 'target': target})
    request = '''POST /submit HTTP/1.1
User-Agent: python-requests/2.24.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Content-Length: %d
Content-Type: application/x-www-form-urlencoded

%s''' % (len(data), data)
    connected = False
    while not connected:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((Config.Backend.WebService.ip, Config.Backend.WebService.port))
            connected = True
        except:
            continue
    s.send((request + '\n').encode())
    s.close()
