def set_redirect_flow_rule(roule_id, compromised_server, server_redundant, src_switch__dst_switch__port):
    flow_rule = {
        "flow": {
            "id": roule_id,
            "match": {
                "ethernet-match": {
                    "ethernet-destination": {
                        "address": compromised_server.host.mac
                    },
                    "ethernet-type": {
                        "type": "2048"
                    }
                }
            },
            "table_id": "0",
            "priority": "35768",
            "instructions": {
                "instruction": {
                    "order": "0",
                    "apply-actions": {
                        "action": [
                            {
                                "order": "0",
                                "set-field": {
                                    "ipv4-destination": server_redundant.host.ip + "/32"
                                }
                            },

                            {
                                "order": 1,
                                "set-field": {
                                    "ethernet-match": {
                                        "ethernet-destination": {
                                            "address": server_redundant.host.mac
                                        }
                                    }
                                }
                            },

                            {
                                "order": "2",
                                "output-action": {
                                    "output-node-connector": src_switch__dst_switch__port,
                                    "max-length": "0"
                                }
                            }

                        ]
                    }
                }
            }
        }
    }
    return flow_rule
