
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
import sys

print "Enter no. of switches:"
x=raw_input()
print "Enter no. of host:"

var=raw_input()
switchlist=[]
hostlist=[]
class MyTopo(Topo):
	def __init__(self,**opts):
		"create custom topo"
		super(MyTopo,self).__init__(**opts)
		
		for i in range (0,int(x)):
			Sname = 's'+str(i)
			switchlist.append(self.addSwitch(Sname))
		
		for i in range (0,int(var)):
			Hname= 'h' + str(i)
			hostlist.append(self.addHost(Hname))
		
		
		for index in range (0,len(switchlist)):
			if(index == len(switchlist)-1):
				break;
			
			self.addLink(switchlist[index],switchlist[index+1])
		
		i=0
		for j in range(len(switchlist)):
			self.addLink(hostlist[i],switchlist[j],bw=1,delay='5ms',loss=1,max_quque_size=1000,use_htb=True)
			i=i+1
			self.addLink(hostlist[i],switchlist[j],bw=2)
			i=i+1



topo = MyTopo()
net =Mininet(topo=topo,host=CPULimitedHost,link=TCLink,controller=OVSController)
count=1
for i in range(0,int(var),2):
	str1="h"
	stri2="10.0.0."
	stri2=stri2+str(count)
	count=count+1
	str1=str1+str(i)
	hi=net.get(str1)
	hi.setIP(stri2,24)

for i in range(1,int(var),2):
	str1="h"
	stri2="192.168.0."
	stri2=stri2+str(count)
	count=count+1
	str1=str1+str(i)
	hi=net.get(str1)
	hi.setIP(stri2,29)
net.start()
dumpNodeConnections(net.hosts)
net.pingAll()
net.stop()
