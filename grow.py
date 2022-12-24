#!/usr/bin/env python

import os
import sys
from typing import List
import subprocess

username = "cathe"
password = ""

dots_git = "https://github.com/thecathe/dots.git"

aur_path = "~/Documents/AUR/"
git_path = "~/Documents/git/"

required_packages = [
    {
        "name": "awesome",
        "version": -1,
        "importance": 1,
        "source": "pacman"
    },
    {
        "name": "xorg-server",
        "version": -1,
        "importance": 1,
        "source": "pacman"
    },
    {
        "name": "xterm",
        "version": -1,
        "importance": 1,
        "source": "pacman"
    },
    {
        "name": "kitty",
        "version": -1,
        "importance": 2,
        "source": "pacman"
    },
    {
        "name": "lightdm",
        "version": -1,
        "importance": 2,
        "source": "pacman"
    },
    {
        "name": "dmenu",
        "version": -1,
        "importance": 5,
        "source": "pacman"
    },
    {
        "name": "polybar",
        "version": -1,
        "importance": 5,
        "source": "pacman"
    },
    {
        "name": "virtualbox-guest-utils",
        "version": -1,
        "importance": 2,
        "source": "pacman"
    },
    {
        "name": "nvim",
        "version": -1,
        "importance": 2,
        "source": "pacman"
    },
    {
        "name": "firefox",
        "version": -1,
        "importance": 5,
        "source": "pacman"
    },
    {
        "name": "picom",
        "version": -1,
        "importance": 3,
        "source": "pacman"
    },
    {
        "name": "nitrogen",
        "version": -1,
        "importance": 3,
        "source": "pacman"
    },
    {
        "name": "emacs",
        "version": -1,
        "importance": 5,
        "source": "pacman"
    },
    {
        "name": "visual-studio-code-bin ",
        "version": -1,
        "importance": 5,
        "source": "https://aur.archlinux.org/visual-studio-code-bin.git"
    },
    {
        "name": "code-features",
        "version": -1,
        "importance": 5,
        "source": "https://aur.archlinux.org/code-features.git"
    },
    {
        "name": "code-git",
        "version": -1,
        "importance": 5,
        "source": "https://aur.archlinux.org/code-git.git"
    }
]

itinerary = {
    "awesome-setup": [
        "mkdir ~/.config/awesome",
        "cp /etc/xdg/awesome/rc.lua ~/.config/awesome/rc.lua"
    ],
    "lighdm-setup": [
        "sudo group -r autologin",
        "sudo gpasswd -a cathe autologin",
        "systemctl enable lightdm.service"
    ]
}

path_cache = {
    "configs": {
        "lightdm": {
            "initial": "/etc/",
            "relative": "lightdm/lighdm.conf"
        },
        "awesome": {
            "initial": "/etc/xdg/",
            "relative": "awesome/rc.lua"
        },
    }
}


def load_file_contents(_path) -> List[dict]:
    ret = []
    f = open(_path, "r")
    for line in f:
        ret.append({"changed": False, "content": line})
    f.close()
    return ret


def build_initial_path(_dict) -> str:
    return f'{_dict["initial"]}{_dict["relative"]}'


if __name__ == "__init__":

    dots_exists = False
    for git_dir in os.listdir(git_path):
        if os.path.isfile(os.path.join(git_path, git_dir)):
            if dots_exists := git_dir == "dots":
                break
    if not dots_exists:
        os.system(f"git clone {dots_git} {os.path.join(git_path,'dots')}")
