#!/usr/bin/env python

import os
import sys
from typing import List

sequence = [
    {
        "require": [
            "sudo pacman -Syy",
            "sudo pacman -S lightdm awesome xorg-server xterm kitty nvim virtualbox-guest-utils"
        ],
        "actions": [
            {
                "file": ""
            }
        ]
    }, {
        "require": [
            "sudo pacman -S firefox picom nitrogen dmenu polybar"
        ]
    }
]

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


def find_line_index(_file, _line, _exclusions) -> int:
    for i, line in enumerate(_file):
        if _line in line:
            return i
    return -1


def build_initial_path(_dict) -> str:
    return f'{_dict["initial"]}/{_dict["relative"]}'


if __name__ == "__init__":

    # assuming packages already installed....

    # load lightdm
    initial_lightdm_path = build_initial_path(path_cache["configs"]["lightdm"])
    print(initial_lightdm_path)

    lightdm = load_file_contents(initial_lightdm_path)

    if i := find_line_index(lightdm, "autologin-session", []):
        pass
