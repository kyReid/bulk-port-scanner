from itertools import islice
from random import randint
from multiprocessing import Pool
import socket
import json

# add all the ports you want to scan for
PORTS = []

def ics_scanner(ip_list):
    """
    Runs a list of IPs against specific ports known to be associated with ICS components.
    :return: prints list of open ports for each IP
    """
    ics_dict = {}
    for ip in ip_list:
        ics_ports = []
        for port in PORTS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((ip, port))
                if result == 0:
                    ics_ports.append(port)
            except Exception as e:
                print(f"ERROR: {e}")
        ics_dict[ip] = ics_ports
    return ics_dict


def random_list_chunk(li, min_chunk=1, max_chunk=100):
    it = iter(li)
    while True:
        nxt = list(islice(it, randint(min_chunk, max_chunk)))
        if nxt:
            yield nxt
        else:
            break


def use_procs():
    p_pool = Pool(len(ip_list))
    p_results = p_pool.map(
        ics_scanner, [
            ip_list[x] for x in range(
                0, len(ip_list))])
    p_pool.close()
    p_pool.join()
    return p_results


if __name__ == "__main__":
    print("Progress: Scan in progress")
    # hard coded filename, can change or use the filename that contains the IPs to scan
    with open('ips.txt', "r") as file:
        ip_list = [line.strip() for line in file]
    ip_list = list(random_list_chunk(ip_list))
    res = use_procs()
    print(type(res))
    print(res)
    ip_dict = {}
    for r in res:
        ip_dict.update(r)
    # hard coded output to a json file
    with open("output.json", "w+") as file:
        file.write(json.dumps(ip_dict, indent=4))
        print("Progress: Scan complete")
