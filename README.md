# Yet<sup><span style="color:red">2</span></sup> another flag submitter

This is yet yet another flag submitter, written in Python.

This tool was written for the CyberChallenge 2020 A/D CTF final by the team of the University of Bologna.

---

### How does it work?
[Working](./submitter.svg)

---

### Configuration (`config.py`)

#### `class CTF:`
- `tick` A round lenght in seconds
- `start` The CTF start timestamp in UTC

#### `class Exploiter:`
- `PoolSize` The size of the multithreading Pool containing the Process that spawns the (Exploit,Target) pair.
The max value should be `number_of_exploits * number_of_targets`.
- `timeout` After how many seconds an exploit is killed.

- ##### `class CustomTimeouts:`
    - `exploit_example` After how many seconds the exploit `exploit_example` is killed. This overrides the default `timeout`.

#### `class Backend:`
- ##### `class Mongo:`
    - `ip` The ip of the Mongo server.
    - `port` The port of the Mongo server.
- ##### `class WebService:`
    - `ip` The ip of the WebService. This ip is also sourced by the WebService itself.
    - `port` The port of the WebService. This port is also sourced by the WebService itself.

#### `class Frontend:`
- `ip` The ip of the Frontend webserver. This ip is also sourced by the Frontend itself.
- `port` The port of the Frontend webserver. This port is also sourced by the Frontend itself.

#### `class Flag:`
- `regex` The regex of the flags. Only matching flags are submitted to the Gameserver.

#### `class Submission:`
- `ip` The ip of the Submission server.
- `port` The port of the Submission server.
- `protocol` The submission protocol used. ( HTTP / Plaintext )
- `url` The Submission URL (if HTTP is used).
- `n_workers` How many processes that submit flags.
- `flag_limit` How many flags are retrieved from the database before being submitted.

`exploits_dir` The absolute path to the directory containing the exploits.  
`targets_file` The absolute path to the plaintext file containing the list of targets (IP).  
`team_ip` Our vulnbox ip, so we don't exploit ourselves.  
