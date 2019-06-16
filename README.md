# onms_bot
open NMS webex bot


how to use it in your project:

from onms_client import onms_client

client = onms_client()

client.get_METHODS()

client.get_vm_list() #returns a dictionary of {
                "req": "vmware-ixc-vcenter.cisco.com", >> requestion name for API calls
                "fid": "vm-1031", >> foreign-id for API calls
                "nlabel": "EMEAR-SE.cisco.com", >> node-label for the name of the node
                "ip": "10.113.108.19" >> interfaces in the 10.*.*.* range
                }

client.get_vm_name() #returns a string OUTPUT >> 'EMEAR-SE.cisco.com'

client.get_vm_status() #returns a dictionary OUTPUT >> {'VMware-ManagedEntity': 'up', 'SSH': 'up', 'ICMP': 'up', 'HTTP': 'up'}

client.get_vm_http_latency() #returns a string of the http latency OUTPUT >> "172.5 ms" this is in milisecond, if there was no value from the API call output will be "no value"

client.get_wan_latency() #returns a string of the WAN latency to london >> "140.4 ms" this is microsecond please convert, if there was no value from the API call output will be "no value"
