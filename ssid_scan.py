import subprocess

INTERFACE = 'wlan0'


def scan(interface: str = None) -> list[dict[str, str]]:
    """iwlist scan wrapper - returns list of available SSIDs, with details"""
    if not interface:
        interface = INTERFACE
    wnetworks = subprocess.run(['iwlist', interface, 'scanning'],
                               capture_output=True, text=True)
    ssids = []
    for line in wnetworks.stdout.splitlines():
        line = line.lstrip()
        if line.startswith(interface):
            continue
        if line.startswith('Cell'):
            wnet = {}
            cell, addr = map(str.strip, line.split('-'))
            wnet['cell'] = cell.split()[-1]
        elif line.startswith('Frequency'):
            wnet['freq'] = line.split(':', 1)[-1]
        elif line.startswith('Quality'):
            a, b = map(int, line[8:].split()[0].split('/'))
            wnet['qual'] = f"{int(round(a/b*100, 0))}%"
        elif line.startswith('ESSID'):
            wnet['ssid'] = line.split(':', 1)[-1].strip('"')
        elif line.startswith('Mode'):
            # using this as our marker of end of relevant info
            ssids.append(wnet)
    return ssids
