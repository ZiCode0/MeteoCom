from netifaces import interfaces, ifaddresses, AF_INET
from requests import get


def get_ip_dict():
    addr = {}
    for interface_name in interfaces():
        addresses = [i['addr'] for i in ifaddresses(interface_name).setdefault(AF_INET, [{'addr': 'no ip addr'}])]
        addr[interface_name] = addresses[0]
    try:
        addr['external'] = get_external_ip()
    except:
        pass
    return addr


def get_external_ip():
    ip = get('https://api.ipify.org', timeout=10).text
    return ip
