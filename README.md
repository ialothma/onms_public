# onms_public
open NMS webex bot


how to use it in your project:

from onms_client import onms_client

client = onms_client()

client.get_METHODS()

client.get_vm_list() #returns a dictionary of {
                "req": "VCENTER URL", >> requestion name for API calls
                "fid": "vm-1031", >> foreign-id for API calls
                "nlabel": "HOSTNAME", >> node-label for the name of the node
                "ip": "10.*.*.*" >> interfaces in the 10.*.*.* range
                }

client.get_vm_name() #returns a string OUTPUT
>> 'HOSTNAME'

client.get_vm_status() #returns a dictionary OUTPUT
>> {'VMware-ManagedEntity': 'up', 'SSH': 'up', 'ICMP': 'up', 'HTTP': 'up'}

client.get_vm_http_latency() #returns a string of the http latency OUTPUT
>> "172.5 ms" this is in milisecond, if there was no value from the API call output will be "no value"

client.get_wan_latency() #returns a string of the WAN latency to london
>> "140.4 ms" this is microsecond please convert, if there was no value from the API call output will be "no value"

client.onms_graph_return() #returns graphs of HTTP latency and WAN latency

client.get_vm_list() #returns a list of all available VMs
>>{'req': 'VCENTER HOSTNAME', 'fid': 'vm-1332', 'nlabel': 'HOSTNAME', 'ip': []}
{'req': 'VCENTER HOSTNAME', 'fid': 'vm-1429', 'nlabel': 'HOSTNAME', 'ip': []}

client.search_vm_list([Keyword-Contained-In-Node-Label]) #returns a list of node labels that contain the Keyword
>> ['HOSTNAME']

client.add_vm_to_watchlist([node-label]) #adds the specified node to the watch list and then returns watch_list
>> [{'req': 'VCENTER HOSTNAME', 'fid': 'vm-1031', 'nlabel': 'HOSTNAME', 'ip': '10.*.*.*'}, 
{'req': 'VCENTER HOSTNAME', 'fid': 'vm-1032', 'nlabel': 'HOSTNAME', 'ip': ['10.*.*.*']}]
