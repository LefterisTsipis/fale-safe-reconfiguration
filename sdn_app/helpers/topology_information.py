
def topologyInformation(data):
    switch = {}
    deviceMAC= {}
    deviceIP = {}
    hostPorts= {}
    linkPorts= {}

    for i in data["network-topology"]["topology"]:

        if "node" in i:
            for j in i["node"]:
                # Device MAC and IP
                if "host-tracker-service:addresses" in j:
                    for k in j["host-tracker-service:addresses"]:
                        ip = k["ip"]
                        mac = k["mac"]
                        deviceMAC[ip] = mac
                        deviceIP[mac] = ip

                # Device Switch Connection and Port
                if "host-tracker-service:attachment-points" in j:

                    for k in j["host-tracker-service:attachment-points"]:
                        mac = k["corresponding-tp"]
                        mac = mac.split(":", 1)[1]
                        ip = deviceIP[mac]
                        temp = k["tp-id"]
                        switchID = temp.split(":")
                        port = switchID[2]
                        hostPorts[ip] = port
                        switchID = switchID[0] + ":" + switchID[1]
                        switch[ip] = switchID

        # Link Port Mapping
    for i in data["network-topology"]["topology"]:
        if "link" in i:
            for j in i["link"]:
                if "host" not in j['link-id']:
                    src = j["link-id"].split(":")
                    srcPort = src[2]
                    dst = j["destination"]["dest-tp"].split(":")
                    srcToDst =src[0] + ":" + src[1] + "::" + dst[0] +":" + dst[1]
                    linkPorts[srcToDst] = srcPort

    return dict(host_mac_info=deviceMAC, host_switch_mapping=   switch, host_port_mapping_to_switch=hostPorts,src_switch__dst_switch__port=linkPorts)