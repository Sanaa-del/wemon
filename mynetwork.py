#!/usr/bin/python

from mininet.node import Controller, Host
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call
import time


def myNetwork():

    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6653)

    info( '*** Add switches/APs\n')
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid',
                             channel='1', mode='g', position='477.0,241.0,0')

    info( '*** Add hosts/stations\n')
    server = net.addHost('server', cls=Host, ip='10.0.0.2', defaultRoute=None, cpu=0.5)
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='480.0,241.0,0',cpu=0.5)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(server, ap1 ,loss=10, delay='300ms', bw=3.0)

    #net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    net.addNAT().configDefault()
    net.start()
    info('*** Adding delay to the wireless link\n')
    # Adding delay to sta1's wireless interface
    sta1.cmd('tc qdisc add dev sta1-wlan0 root netem delay 500ms')

    info( '*** Starting switches/APs\n')
    net.get('ap1').start([c0])

    info( '*** Post configure nodes\n')

    appServer = net.get('server')
    wd = str(appServer.cmd("pwd"))[:-2]

    # with open('confFileContent.txt') as f:
    #     confFileContent = f.read()
    
    # appServer.cmd("echo 'events { } http { server { listen " + appServer.IP() + ":81; root /var/www/websites; " + confFileContent + "} }' > nginx-conf.conf") # Create server config file
    # appServer.cmd("sudo nginx -c " + wd + "/nginx-conf.conf") # Tell nginx to use configuration from the file we just created
    # time.sleep(1) # Server might need some time to start

    # appServer.cmd("sudo apt install nginx")

    # Start the iperf server on 'server' host
    info('*** Configuring Nginx on the server\n')
    # Configure Nginx using the specified config file. Adjust the path as necessary.
    server.cmd('nginx -c /home/sghandi/Téléchargements/wemon-main/nginx-conf.conf')

# Test the Nginx configuration
    server.cmd('nginx -t')

# Instead of using systemctl to reload Nginx, directly restart Nginx
# This is necessary because systemctl commands may not work as expected in Mininet's simulated environments
    server.cmd('nginx -s reload') # or 'nginx -s stop' followed by 'nginx'

    time.sleep(10) 
    
    
    
    server.cmd('iperf -s &')
    #net.pingAll()
    #CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
