import os
import socket
from lxml import etree

class Ganglia_Ceilometer_Plugin():
    
    results = {}
    #init method, do nothing now
    def __init__(self):    
        print "Start Ganglia Ceilometer Connection Plugin."

    #read ganglia metrics with ganglia ip and port, output the byte stream
    def read_ganglia(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	data = ""
	while True:
            bytes = s.recv(4096)
            if len(bytes) == 0:
                break;
            data += bytes
        s.close()
        return data

    #read metrics with XML parser, support multiple hosts, get all metrics with values 
    def parse_ganglia(self, s):
        hosts = {}
        root = etree.XML(s)
        for host in root.iter('HOST'):
            name = host.get('NAME')
            hosts[name] = {}
            metrics = hosts[name]
            for m in host.findall('METRIC'):
                metrics[m.get('NAME')] = m.attrib.get("VAL")
        return hosts
   
    #read ganglia metrics and parse into tuples, currently just name and value, cpu metrics now
    def get_xml_from_ganglia(self, host, port):
	s = self.read_ganglia(host, port)
        hosts = self.parse_ganglia(s)
	for h in hosts:
            keys = sorted(hosts[h])
            for k in keys:
		if "cpu_" in k:
		    self.results[k] = hosts[h][k]
                    print "   %s = %s" % (k,hosts[h][k])
	return self.results

#def main():
    #currently test case, ganglia is installed locally, port is 8649 for default
#    gcp = Ganglia_Ceilometer_Plugin()
#    gcp.get_xml_from_ganglia("localhost", 8649)
#    print gcp.results

#if __name__ == "__main__":
#    main()
