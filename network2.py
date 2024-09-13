#!/usr/bin/env python

import sys
import csv
import subprocess
from mn_wifi.cli import CLI
from mininet.node import Controller, Host
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
import time




def configure_interference(ap, interfering_node, medium_availability):
    # Define UDP rates corresponding to medium availability percentages
    udp_rates = {
        100: '0mbps',  # No interference check this 
        70: '10mbps',
        50: '20mbps',
        30: '30mbps',
        15: '40mbps'
    }

    # Get the UDP rate for the desired medium availability
    udp_rate = udp_rates.get(medium_availability, '10mbps')  # Default to 70% if not found

    # Stop any previous iperf processes to clear interference if switching to no interference
    interfering_node.cmd('pkill iperf')
    ap.cmd('pkill iperf')

    if medium_availability != 100:
        # Start the iperf server on the AP (listens for UDP traffic)
        ap.cmd('iperf -s -u -p 5001 &')

        # Start the iperf client on the interfering node to generate UDP traffic to the AP
        interfering_node.cmd(f'iperf -c {ap.IP()} -u -b {udp_rate} -t -1 -i 1 -p 5001 &')
        
        
        

def myNetwork(server_cpu_v=1, fading_v=3, delay_v='0ms', loss_v=0, bw_v=100, client_cpu_v=1, medium_availability_v=100, experiment_id=None):

    setLogLevel('info')
    net = Mininet_wifi(topo=None, build=False, link=wmediumd, wmediumd_mode=interference, ipBase='10.0.0.0/8')

    info('*** Adding controller\n')

    c0 = net.addController(name='c0', controller=Controller, protocol='tcp', port=6653)

    info('*** Add switches/APs\n')
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid', channel='1', mode='g', position='477.0,241.0,0')

    info('*** Add hosts/stations\n')
    server = net.addHost('server', cls=Host, ip='10.0.0.2', defaultRoute=None, cpu=server_cpu_v)
    sta1 = net.addStation('sta1', ip='10.0.0.1', position='480.0,241.0,0', cpu=client_cpu_v)
 # Add an interfering station
    sta2 = net.addStation('sta2', ip='10.0.0.3', position='470.0,241.0,0', cpu=1)

    info('*** Configuring Propagation Model\n')
    net.setPropagationModel(model="logDistance", exp=fading_v)

    info('*** Configuring wifi nodes\n')
    net.configureWifiNodes()

    info('*** Add links\n')
    net.addLink(server, ap1, loss=loss_v, delay=delay_v, bw=bw_v)

    #net.plotGraph(max_x=1000, max_y=1000)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    net.addNAT().configDefault()
    net.start()
  
    
    #info('*** Adding delay to the wireless link\n')
    #sta1.cmd('tc qdisc add dev sta1-wlan0 root netem delay 500ms')

    info('*** Starting switches/APs\n')
    net.get('ap1').start([c0])
    
    # Configure medium availability
    configure_interference(ap1, sta2, medium_availability_v)

    info('*** Post configure nodes\n')
    
    appServer = net.get('server')
    wd = str(appServer.cmd("pwd"))[:-2]
    
    info('*** Configuring Nginx on the server\n')
    server.cmd('nginx -c /home/sghandi/Téléchargements/wemon-main/nginx-conf4.conf')
    server.cmd('nginx -t')
    server.cmd('nginx -s reload')

    time.sleep(3)
    
    # Example of setting HTB qdisc with adjusted r2q
    #sta1.cmd('tc qdisc add dev sta1-wlan0 root handle 1: htb default 10 r2q 100')
    #sta1.cmd(f'tc class add dev sta1-wlan0 parent 1: classid 1:1 htb rate {bw_v}mbit quantum 10000')

    # Perform ping test
    print('Starting the ping test to server')
    ping_result = subprocess.run(['ping', '-c', '5', server.IP()],           capture_output=True, text=True)
    print(ping_result.stdout)  # Print only the standard output

   # Use a different port for iperf performance measurement
    test_port = 5002

    # Measure TCP downlink from server to sta1
    info('Measuring TCP Downlink (server to sta1)\n')
    sta1.cmd(f'iperf -s -D -p {test_port}')  # Start iperf server on sta1 in daemon mode (background)
    downlink_result_tcp = server.cmd(f'iperf -c {sta1.IP()} -p {test_port} -t 10')
    print('TCP Downlink result:', downlink_result_tcp)
    sta1.cmd('pkill iperf')  # Stop iperf server on sta1

    # Measure TCP uplink from sta1 to server
    info('Measuring TCP Uplink (sta1 to server)\n')
    server.cmd(f'iperf -s -D -p {test_port}')  # Start iperf server on server in daemon mode (background)
    uplink_result_tcp = sta1.cmd(f'iperf -c {server.IP()} -p {test_port} -t 10')
    print('TCP Uplink result:', uplink_result_tcp)
    server.cmd('pkill iperf')  # Stop iperf server on server

    # Measure UDP downlink from server to sta1
    info('Measuring UDP Downlink (server to sta1)\n')
    server.cmd(f'iperf -s -u -D -p {test_port}')  # Start UDP iperf server in daemon mode
    udp_downlink_result = sta1.cmd(f'iperf -c {server.IP()} -u -b 10M -p {test_port} -t 10')
    print('UDP Downlink result:', udp_downlink_result)
    server.cmd('pkill iperf')  # Stop UDP iperf server on server

    # Measure UDP uplink from sta1 to server
    info('Measuring UDP Uplink (sta1 to server)\n')
    sta1.cmd(f'iperf -s -u -D -p {test_port}')  # Start UDP iperf server on sta1 in daemon mode
    udp_uplink_result = server.cmd(f'iperf -c {sta1.IP()} -u -b 10M -p {test_port} -t 10')
    print('UDP Uplink result:', udp_uplink_result)
    sta1.cmd('pkill iperf')  # Stop UDP iperf server on sta1
    
    
   
    
    with open('results_final.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([experiment_id, udp_uplink_result, udp_downlink_result, 
                         uplink_result_tcp, downlink_result_tcp, ping_result.stdout])


    # When done, create the flag file
    flag_file = '/tmp/mininet_done.flag'
    open(flag_file, 'a').close()
    
      # Stop the network
    net.stop()
    

  
  

   
   
   
def main():
    if len(sys.argv) < 2:
        print("Error: No input provided.")
        sys.exit(1)
    #print('le nombre de parametres:', len(sys.argv))
    input_line = sys.argv
    parameters = input_line
    #print('les parametres:', parameters)
    #print('len les parametres:', len(parameters))
    if len(parameters) != 9:
        print("Error: Incorrect number of parameters provided.")
        sys.exit(1)

    experiment_id=float(parameters[1])
    server_cpu_v = float(parameters[2])
    #print('cpu serv ', server_cpu_v)
    fading_v = int(parameters[3])
    #print('fading_v ', fading_v)
    delay_v = parameters[4]
    #print('delay_v ', delay_v)
    loss_v = float(parameters[5])
    #print('loss_v ', loss_v)
    bw_v = float(parameters[6])
    #print('bw_v ', bw_v)
    client_cpu_v = float(parameters[7])
    medium_availability_v = float(parameters[8])
    #print('client_cpu_v ', client_cpu_v)
    
    myNetwork(server_cpu_v=server_cpu_v, fading_v=fading_v, delay_v=delay_v,
              loss_v=loss_v, bw_v=bw_v, client_cpu_v=client_cpu_v, medium_availability_v=medium_availability_v,experiment_id=experiment_id)

               

if __name__ == '__main__':
    main()
    
