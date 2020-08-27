import re
from subprocess import CalledProcessError, check_output as echo
from sys import platform

#Initialize constants and variables
FILENAME = "configuracion.txt"
IP = "192.168.0."
GETMACFROMFILE = True
fnd_mac_addresses = []

#Initialize functions
def getMacsFromNMAP(ip):
    addresses = []

    NMAP_SN = "nmap -sn "
    MAC_CODE_NMAP = slice(13,30)

    for line in echo(NMAP_SN + ip + "*").decode().splitlines():
        if "MAC" in line:
            addresses.append(line[MAC_CODE_NMAP])
    
    return addresses

def getMacsFromARP(ip):
    addresses = []

    ARP_CM = ["arp", "-a"]
    MAC_CODE_ARP = slice(23,41)

    for line in echo(ARP_CM).decode().splitlines()[2:]:
        if ip in line:
            macAddress = line[MAC_CODE_ARP].replace(" ","").replace("-",":").upper()
            addresses.append(macAddress)
    
    return addresses

def getMacAddressesFromFile(fileName):
    macAddressDic = {}
    configFile = open(FILENAME, "r")
    if configFile.readable():
        for line in configFile:
            if ":" in line:
                data = line.split(":")
                macAddress = data[0].replace(" ","").replace("-",":").upper()
                macOwner = data[1].replace(" ","").replace("\n","")
                macAddressDic[macAddress] = macOwner
    configFile.close()
    return macAddressDic

# Initialize file info
try:
    macAddressDic = getMacAddressesFromFile(FILENAME) if GETMACFROMFILE else {}
except:
    GETMACFROMFILE = False
    print('Could not find file ' + FILENAME)

#Program Start
if 'win' in platform:
    ## NMAP
    try:
        [fnd_mac_addresses.append(mac) for mac in getMacsFromNMAP(IP) if mac not in fnd_mac_addresses]
    except:
        print('Could not excecute NMAP program')

    ## ARP
    try:
        [fnd_mac_addresses.append(mac) for mac in getMacsFromARP(IP) if mac not in fnd_mac_addresses]
    except:
        print('Could not excecute ARP program')

    ## ARPSCAN
    #try:
    #    [fnd_mac_addresses.append(mac) for mac in getMacsFromARPSCAN(IP) if mac not in fnd_mac_addresses]
    #except:
    #    print('Could not excecute ARP program')
    

for mac in fnd_mac_addresses:
    if(GETMACFROMFILE):
        if mac in macAddressDic:
            print(macAddressDic[mac])
    else:
        print(mac)