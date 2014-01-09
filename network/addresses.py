import json
auto_auto={
    "interface": "ge",
    "ssid": "test",
    "ipv4": {
        "mode": "auto",
        "address": "",
        "netmask": "",
        "gateway": ""
    },
    "ipv6": {
        "mode": "auto",
	    "address": "",

        "netmask": "",
        "gateway": ""
    }
}
auto_static={
    "interface": "ge",
    "ssid": "test",
    "ipv4": {
        "mode": "auto",
        "address": "",
        "netmask": "",
        "gateway": ""
    },
    "ipv6": {
        "mode": "static",
	    "address": "2001::4",
        "netmask": "64",
        "gateway": "2004::1"
    }
}
static_auto={
    "interface": "ge",
    "ssid": "test",
    "ipv4": {
        "mode": "static",
        "address": "10.7.3.100",
        "netmask": "255.255.255.0",
        "gateway": "10.7.3.1"
    },
    "ipv6": {
        "mode": "auto",
	    "address": "",
        "netmask": "",
        "gateway": ""
    }
}
static_static={
    "interface": "ge",
    "ssid": "test",
    "ipv4": {
        "mode": "static",
        "address": "10.7.3.100",
        "netmask": "255.255.255.0",
        "gateway": "10.7.3.1"
    },
    "ipv6": {
        "mode": "static",
	    "address": "2004::4",
        "netmask": "64",
        "gateway": "2004::1"
    }
}

print json.dumps(auto_auto,separators=(',', ':'))
print json.dumps(auto_static,separators=(',', ':'))
print json.dumps(static_auto,separators=(',', ':'))
print json.dumps(static_static,separators=(',', ':'))