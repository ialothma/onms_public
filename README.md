# onms_bot
open NMS webex bot


how to use it in your project:

from onms_client import onms_client

client = onms_client()

client.get_METHODS()

client.get_wan_latency() #returns a dictionary {'VMware-ManagedEntity': 'up', 'SSH': 'up', 'ICMP': 'up', 'HTTP': 'up'}
client.get_vm_http_stats() #returns an integer of the http latency
client.get_wan_latency() #returns an integer of the WAN latency to london
