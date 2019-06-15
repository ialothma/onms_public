import requests
from requests.auth import HTTPBasicAuth
import json

class onms_client:

    def __init__(self):
        self.req_header = {'accept':'application/json'}
        self.hostname = "nms.cisco.com"
        self.port = "8980"
        self.username = "onms_api"
        self.password = "onms_api_123"
        self.req_auth = HTTPBasicAuth("onms_api","onms_api_123")
        self.onms_url = "http://{0}:{1}/opennms/rest".format(self.hostname,self.port)

    #def get_node_list(self):
    def get_vm_name(self):
        request_url = "{0}/nodes/519".format(self.onms_url)

        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)

        vm_name= data['label']

        return vm_name

    def get_vm_status(self):
        request_url = "{0}/nodes/519/ipinterfaces/10.113.108.19/services".format(self.onms_url)
        api_call = requests.get(request_url, headers=self.req_header,auth=self.req_auth)
        data = json.loads(api_call.text)
        services = {}
        for temp in data['service']:
            if temp['statusLong'] == "Managed":
                if temp['down']==False:
                    services[temp['serviceType']['name']] = 'up'
                else:
                    services[temp['serviceType']['name']] = 'down'

        return services

    def get_vm_http_latency(self):
        request_url = "{0}/measurements/node[vmware-ixc-vcenter.cisco.com:vm-1031].responseTime[10.113.108.19]/http?start=-60000".format(self.onms_url)
        api_call = requests.get(request_url, headers=self.req_header,auth=self.req_auth)
        data = json.loads(api_call.text)
        #last value
        for temp in reversed(data['columns'][0]['values']):
            if temp != 'NaN':
                http_response_latency = temp
                return http_response_latency

        return "no value"


    def get_wan_latency(self):
        request_url = "{0}/measurements/node[London IXC - Network Devices:1560421929244].responseTime[10.51.47.254]/icmp?start=-600000".format(self.onms_url)
        api_call = requests.get(request_url, headers=self.req_header,auth=self.req_auth)
        data = json.loads(api_call.text)
        #last value
        for temp in reversed(data['columns'][0]['values']):
            if temp != 'NaN':
                wan_latency=temp
                return wan_latency

        return "no value"




"""
http://nms.cisco.com:8980/opennms/rest/measurements/node%5Bvmware-ixc-vcenter.cisco.com:vm-1031%5D.responseTime%5B10.113.108.19%5D/http

http://nms.cisco.com:8980/opennms/rest/measurements/node%5Bvmware-ixc-vcenter.cisco.com:vm-1031%5D.responseTime%5B10.113.108.19%5D/http


http_latency = r'http://nms.cisco.com:8980/opennms/rest/measurements/node[vmware-ixc-vcenter.cisco.com:vm-1031].responseTime[10.113.108.19]/http?start=-60000'
wan_latency = r'http://nms.cisco.com:8980/opennms/rest/measurements/node[London IXC - Network Devices:1560421929244].responseTime[10.51.47.254]/icmp?start=-600000'
vm_status = r'http://nms.cisco.com:8980/opennms/rest/nodes/519/ipinterfaces/10.113.108.19/services'
vm_status = r'http://nms.cisco.com:8980/opennms/rest/nodes/519/ipinterfaces/10.113.108.19/services'
req_header = {'accept':'application/json'}
req_auth = HTTPBasicAuth("onms_api","onms_api_123")
response = requests.get(req_url,headers=req_header,auth=req_auth)

def api_call(req_url):
    req_header = {'accept':'application/json'}
    req_auth = HTTPBasicAuth("onms_api","onms_api_123")
    response = requests.get(req_url,headers=req_header,auth=req_auth)
    data = json.loads(response.text)
    return json.dumps(data, indent=4, sort_keys=True)
"""
