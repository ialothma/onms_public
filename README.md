# onms_bot
open NMS webex bot


how to use it in your project:

from onms_client import onms_client

client = onms_client()

client.get_METHODS()

client.get_vm_list() #returns a list of VM names

client.get_vm_name() #returns a string OUTPUT >> 'EMEAR-SE.cisco.com'

client.get_vm_status() #returns a dictionary OUTPUT >> {'VMware-ManagedEntity': 'up', 'SSH': 'up', 'ICMP': 'up', 'HTTP': 'up'}

client.get_vm_http_latency() #returns a float of the http latency OUTPUT >> 172.50803392 this is in milisecond

client.get_wan_latency() #returns z float of the WAN latency to london >> 140442.61666666667 this is microsecond please convert
