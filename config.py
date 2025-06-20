# config.py

SERVERS = {
    "remote1": {
        "host": "192.168.1.101",
        "disk": "/dev/sdb"
    },
    "remote2": {
        "host": "192.168.1.102",
        "disk": "/dev/sdc"
    },
    "remote3": {
        "host": "192.168.1.103",
        "disk": "/dev/sdd"
    }
}

# Default user to SSH as (optional if you want to make this dynamic later)
SSH_USER = "root"
