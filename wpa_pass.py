import subprocess
from os.path import exists
import argparse

WPA_CONF_HEAD = '# UNCONFIGURED WPA_SUPPLICANT'
WPA_CONF_XTRA = '# remove the above line if you edit this file'
WPA_SUP_CNF_PATH = '/etc/wpa_supplicant/wpa_supplicant.conf'


class WpaConfError(Exception):
    pass


def set_wifi_creds(ssid: str, password: str) -> None:
    """wpa_passphrase wrapper to write wpa_supplicant.conf"""
    if exists(WPA_SUP_CNF_PATH):
        with open(WPA_SUP_CNF_PATH) as fob:
            header = fob.readline()
        if header.rstrip() != WPA_CONF_HEAD:
            raise WpaConfError(f'header missing from {WPA_SUP_CNF_PATH}')

    wpa_pass = subprocess.run(['wpa_passphrase', ssid, password],
                              capture_output=True, text=True)
    if wpa_pass.returncode != 0:
        raise WpaConfError(wpa_pass)
    conf_lines = [WPA_CONF_HEAD+'\n', WPA_CONF_XTRA+'\n\n']
    lines = wpa_pass.stdout.splitlines()
    for line in lines:
        # exclude commented plain text password
        if not line.lstrip().startswith('#psk='):
            conf_lines.append(line+'\n')

    with open(WPA_SUP_CNF_PATH, 'w') as fob:
        fob.writelines(conf_lines)
