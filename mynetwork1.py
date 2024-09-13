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
    server = net.addHost('server', cls=Host, ip='10.0.0.2', defaultRoute=None)
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='480.0,241.0,0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(server, ap1)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    net.addNAT().configDefault()
    net.start()

    info( '*** Starting switches/APs\n')
    net.get('ap1').start([c0])

    info( '*** Post configure nodes\n')

    appServer = net.get('server')
    wd = str(appServer.cmd("pwd"))[:-2]

   
    info('*** Configuring Nginx on the server\n')
    server.cmd('nginx -c /home/sghandi/Téléchargements/wemon-main/nginx-conf.conf')
    server.cmd('nginx -t')
    server.cmd('nginx -s reload') # or 'nginx -s stop' followed by 'nginx'
    time.sleep(1) 
    
    
    
    server.cmd('iperf -s &')
    
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

