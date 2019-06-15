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
        self.onms_url = "http://{0}:{1}/opennms/rest".format(self.hostname,
                                                             self.port)
        self.vCenter = "vmware-ixc-vcenter.cisco.com"
        self.vm_watch_list = [
                                {
                                "req": "vmware-ixc-vcenter.cisco.com",
                                "fid": "vm-1031",
                                "nlabel": "EMEAR-SE.cisco.com",
                                },
                                ]

        self.wan_watch_list = [
                                {
                                "req": "London IXC - Network Devices",
                                "fid": "1560421929244",
                                "nlabel": "BDLK WAN",
                                },
                                ]

    #def get_node_list(self):
    def get_vm_list(self, id=0):
        request_url = "{0}/requisitions/{1}/nodes".format(self.onms_url,
                                                          self.vm_watch_list[id]['req'])

        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)
        vm_list = []
        for temp in data['node']:
            vm_list.append(temp['node-label'])

        return vm_list

    def get_vm_name(self, id=0):
        request_url = "{0}/nodes/{1}:{2}".format(self.onms_url,
                                                 self.vm_watch_list[id]['req'],
                                                 self.vm_watch_list[id]['fid'])
        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)

        vm_name = data['label']

        return vm_name


    def get_vm_status(self, id=0):

        request_url = "{0}/nodes/{1}:{2}/ipinterfaces/10.113.108.19\
                       /services".format(self.onms_url,
                                         self.vm_watch_list[id]['req'],
                                         self.vm_watch_list[id]['fid'])

        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)

        services = {}

        for temp in data['service']:
            if temp['statusLong'] == "Managed":
                if temp['down']==False:
                    services[temp['serviceType']['name']] = 'up'
                else:
                    services[temp['serviceType']['name']] = 'down'

        return services

    def get_latency(self, id, ip, service, start_time, watch_list):
        request_url = "{0}/measurements/node[{1}:{2}].responseTime[{3}]/{4}?start=-{5}".format(self.onms_url,
                                            watch_list[id]['req'],
                                            watch_list[id]['fid'],
                                            ip,
                                            service,
                                            start_time)

        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)
        #last value
        for temp in reversed(data['columns'][0]['values']):
            if temp != 'NaN':
                latency = temp
                return latency

        return "no value"


    def get_vm_http_latency(self, id=0, ip='10.113.108.19', start_time='600000'):

        http_latency = self.get_latency(id, ip, 'http', start_time, self.vm_watch_list)

        return http_latency

    def get_wan_latency(self, id=0, ip='10.51.47.254', start_time='600000'):

        wan_latency = self.get_latency(id, ip, 'icmp', start_time, self.wan_watch_list)

        return wan_latency


#method for debugging
def test():
    c = onms_client()
    print("Checking methods")
    m1 = 'get_vm_list'
    print("Method: {0}".format(m1))
    try:
        print(c.get_vm_list())
    except:
        print("Method: {0} has an error".format(m1))
    else:
        print("Method: {0} is successful".format(m1))

    m2 = 'get_vm_name'
    print("Method: {0}".format(m2))
    try:
        print(c.get_vm_name())
    except:
        print("Method: {0} has an error".format(m2))
    else:
        print("Method: {0} is successful".format(m2))

    m3 = 'get_vm_status'
    print("Method: {0}".format(m3))
    try:
        print(c.get_vm_status())
    except:
        print("Method: {0} has an error".format(m3))
    else:
        print("Method: {0} is successful".format(m3))

    c.get_vm_http_latency()

    m4 = 'get_vm_http_latency'
    print("Method: {0}".format(m4))
    try:
        print(c.get_vm_http_latency())
    except:
        print("Method: {0} has an error".format(m4))
    else:
        print("Method: {0} is successful".format(m4))

    m5 = 'get_wan_latency'
    print("Method: {0}".format(m5))
    try:
        print(c.get_wan_latency())
    except:
        print("Method: {0} has an error".format(m5))
    else:
        print("Method: {0} is successful".format(m5))


#test()


"""
http://nms.cisco.com:8980/opennms/rest/measurements/node%5Bvmware-ixc-vcenter.cisco.com:vm-1031%5D.responseTime%5B10.113.108.19%5D/http

http://nms.cisco.com:8980/opennms/rest/measurements/node%5Bvmware-ixc-vcenter.cisco.com:vm-1031%5D.responseTime%5B10.113.108.19%5D/http


request_url = "{0}/measurements/node[{1}:{2}].responseTime[10.113.108.19]\
                /http?start=-60000".format(self.onms_url,
                                    self.vm_watch_list[id]['req'],
                                    self.vm_watch_list[id]['fid'])

      request_url = "{0}/measurements/node[{1}:{2}].responseTime[10.51.47.254]\
                /icmp?start=-600000".format(self.onms_url,
                                     self.wan_watch_list[id]['req'],
                                     self.wan_watch_list[id]['fid'])

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
