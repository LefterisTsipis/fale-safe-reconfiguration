def set_block_flow_rule(roule_id, compromised_server):
    flow_rule = {
        "flow": [{
            "id": roule_id,
            "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": "2048"
                    }
                },
                "ipv4-destination": compromised_server.host.ip + "/32"
            },
            "instructions": {
                "instruction": [
                    {
                        "apply-actions": {
                            "action": [
                                {
                                    "drop-action": {},
                                    "order": "0"
                                }
                            ]
                        },
                        "order": "0"
                    }
                ]
            },
            "cookie_mask": "255",
            "flow-name": "test",
            "installHw": "false",
            "barrier": "false",
            "strict": "false",
            "priority": "3",
            "idle-timeout": "0",
            "hard-timeout": "0",
            "table_id": "0"
        }]
    }

    return flow_rule
