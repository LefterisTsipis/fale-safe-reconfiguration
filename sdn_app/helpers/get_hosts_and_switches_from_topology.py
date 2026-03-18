def get_hosts_and_switches_from_topology(topology):
    switch = []
    hosts_ip= []
    hosts_mac = []

    for i in topology["network-topology"]["topology"]:

        if "node" in i:
            for j in i["node"]:
                # Device MAC and IP
                if "host-tracker-service:addresses" in j:
                    for k in j["host-tracker-service:addresses"]:
                        hosts_ip.append(k["ip"])
                        hosts_mac.append(k["mac"])
                else:
                    switch.append(j["node-id"])

    return dict(hosts_ip=hosts_ip, hosts_mac=hosts_mac, switch=switch)