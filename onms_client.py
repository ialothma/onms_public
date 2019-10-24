import requests
from requests.auth import HTTPBasicAuth
import json
import mechanicalsoup
import pprint

class onms_client:

    def __init__(self):
        self.req_header = {'accept':'application/json'}
        self.hostname = "" #URL
        self.port = "" #PORT
        self.username = "" #USER
        self.password = "" #PASS
        self.req_auth = HTTPBasicAuth(self.username,self.password)
        self.onms_url = "http://{0}:{1}/opennms/rest".format(self.hostname,
                                                             self.port)
        self.vCenter = "VCENTER URL" #monitored vCenters
        self.vm_list = []
        self.vm_watch_list = [
                                {
                                "req": "vmware-ixc-vcenter.cisco.com",
                                "fid": "vm-1031",
                                "nlabel": "HOSTNAME",
                                "ip": "*.*.*.*"
                                },
                                {
                                "req": "vmware-ixc-vcenter.cisco.com",
                                "fid": "vm-1032",
                                "nlabel": "HOSTNAME",
                                "ip": "*.*.*.*"
                                },{
                                "req": "vmware-ixc-vcenter.cisco.com",
                                "fid": "vm-1724",
                                "nlabel": "HOSTNAME",
                                "ip": "*.*.*.*"
                                }
                                ]

        self.wan_watch_list = [
                                {
                                "req": "London IXC - Network Devices",
                                "fid": "1560421929244",
                                "nlabel": "HOSTNAME",
                                "ip" : "*.*.*.*"
                                },
                                ]

    #def get_node_list(self):

    def get_vm_name(self, id):#get name of specified VM
        request_url = "{0}/nodes/{1}:{2}".format(self.onms_url,
                                                 self.vm_watch_list[id]['req'],
                                                 self.vm_watch_list[id]['fid'])
        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)

        vm_name = data['label']

        return vm_name


    def get_vm_status(self, id):#get status of specified VM

        request_url = "{0}/nodes/{1}:{2}/ipinterfaces/{3}/services".format(self.onms_url,
                                         self.vm_watch_list[id]['req'],
                                         self.vm_watch_list[id]['fid'],
                                         self.vm_watch_list[id]['ip'])

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

    def get_latency(self, id, service, start_time, watch_list):#gets response time metrics
        request_url = "{0}/measurements/node[{1}:{2}].responseTime[{3}]/{4}?start=-{5}".format(self.onms_url,
                                            watch_list[id]['req'],
                                            watch_list[id]['fid'],
                                            watch_list[id]['ip'],
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


    def get_vm_http_latency(self, id, start_time='600000'): #gets HTTP response time metrics
        service = 'http'
        http_latency = self.get_latency(id, service, start_time, self.vm_watch_list)
        if http_latency != 'no value':
            http_latency = "{:.1f} ms".format(http_latency)
        return http_latency

    def get_wan_latency(self, id=0, start_time='600000'): #gets WAN ICMP Response time metrics
        service= 'icmp'
        wan_latency = self.get_latency(id, service, start_time, self.wan_watch_list)
        if wan_latency != 'no value':
            wan_latency = wan_latency/1000#convert to milisecond
            wan_latency = "{:.1f} ms".format(wan_latency)
        return wan_latency

    def onms_graph_return_wan(self): #returns png of HTTP/WAN Graphs
    	browser = mechanicalsoup.Browser()
    	login_page = browser.get("http://ONMS_URL:PORT/opennms/j_spring_security_check")

    	login_form = login_page.soup.find("form")
    	login_form.find("input", {"name": "j_username"})["value"] = "USERNAME"
    	login_form.find("input", {"name": "j_password"})["value"] = "PASSWORD"
    	browser.submit(login_form, login_page.url)

    	resp = browser.session.get("http://ONMS_URL:PORT/opennms/graph/graph.png?resourceId=node%5BLondon+IXC+-+Network+Devices%3A1560421929244%5D.responseTime%5B[REPLACE WITH IP]%5D&start=-3600000&end=0&report=icmp")
    	resp.raise_for_status()

    	with open('icmp.png','wb') as outf:
    		outf.write(resp.content)

    def onms_graph_return_http(self, id): #returns png of HTTP/WAN Graphs
    	browser = mechanicalsoup.Browser()
    	login_page = browser.get("http://ONMS_URL:PORT//opennms/j_spring_security_check")

    	login_form = login_page.soup.find("form")
    	login_form.find("input", {"name": "j_username"})["value"] = "USERNAME"
    	login_form.find("input", {"name": "j_password"})["value"] = "PASSWORD"
    	browser.submit(login_form, login_page.url)

    	resp = browser.session.get("http://ONMS_URL:PORT//opennms/graph/graph.png?resourceId=node[vmware-ixc-vcenter.cisco.com:{}].responseTime[{}]&start=-3600000&end=0&report=http".format(self.vm_watch_list[id]['fid'], self.vm_watch_list[id]['ip']))
    	resp.raise_for_status()

    	with open('http.png','wb') as outf:
    		outf.write(resp.content)


    def get_vm_list(self, id=0):# returns a dictionary of all the VMs in the requestion
        request_url = "{0}/requisitions/{1}".format(self.onms_url,
                                                    self.vm_watch_list[id]['req'])

        api_call = requests.get(request_url,
                                headers=self.req_header,
                                auth=self.req_auth)

        data = json.loads(api_call.text)
        self.vm_list = []
        req = data['foreign-source']
        for temp in data['node']:
            self.vm_list.append(
            {
            "req": req,
            "fid": temp['foreign-id'],
            "nlabel": temp['node-label'],
            "ip": [x['ip-addr'] for x in temp['interface'] if x['ip-addr'] and x['ip-addr'].startswith('10')]
            }
            )

        return self.vm_list


    def search_vm_list(self, keyword): #returns a list of VMs that contain the query string

        result = []
        for temp in self.vm_list:
            if keyword.lower() in temp['nlabel'].lower():
                result.append(temp['nlabel'])

        if result == []:
            result = ['no VM with that name was found']

        return result

    def add_vm_to_watchlist(self, keyword): #adds vm to watchlist with specified node label

        for temp in self.vm_list:
            if keyword.lower() == temp['nlabel'].lower() and temp not in self.vm_watch_list:
                self.vm_watch_list.append(temp)

        return self.vm_watch_list



'''
#method for debugging
def test():
    c = onms_client()
    print("Checking methods")
    m1 = 'get_vm_list'
    print("Method: {0}".format(m1))
    #
    [print(x) for x in c.get_vm_list()]
    try:
        [print(x) for x in c.get_vm_list()]
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

    m5 = 'search_vm_list'
    print("Method: {0}".format(m5))
    try:
        temp = c.search_vm_list("bot")
        print(temp)
    except:
        print("Method: {0} has an error".format(m5))
    else:
        print("Method: {0} is successful".format(m5))

    m5 = 'add_vm_to_watchlist'
    print("Method: {0}".format(m5))
    try:
        print(c.add_vm_to_watchlist(temp[0]))
    except:
        print("Method: {0} has an error".format(m5))
    else:
        print("Method: {0} is successful".format(m5))

    m5 = 'add_vm_to_watchlist_2'
    print("Method: {0}".format(m5))
    try:
        print(c.add_vm_to_watchlist(temp[0]))
    except:
        print("Method: {0} has an error".format(m5))
    else:
        print("Method: {0} is successful".format(m5))

'''

#test()

