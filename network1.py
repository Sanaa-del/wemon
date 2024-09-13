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
        100: '0mbps',  # No interference
        70: '0.7mbps',
        50: '1.1mbps',
        30: '2.1mbps',
        15: '2.9mbps'
    }

    # Get the UDP rate for the desired medium availability
    udp_rate = udp_rates.get(medium_availability, '0.7mbps')  # Default to 70% if not found

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
    sta2 = net.addStation('sta2', ip='10.0.0.3', position='470.0,241.0,0', cpu=client_cpu_v)


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
    info('*** Adding delay to the wireless link\n')
    sta1.cmd('tc qdisc add dev sta1-wlan0 root netem delay 500ms')

    info('*** Starting switches/APs\n')
    net.get('ap1').start([c0])

    # Configure medium availability
    configure_interference(ap1, sta2, medium_availability_v)
    
    info('*** Post configure nodes\n')

    info('*** Configuring Nginx on the server\n')
    server.cmd('nginx -c /path/to/nginx-conf.conf')
    server.cmd('nginx -t')
    server.cmd('nginx -s reload')

    time.sleep(1)

    info('i configured nginx')
    #CLI(net)
    ping_command = 'sudo mn -c && sudo mn --mac --test pingall'

    # Run the ping command
    ping_process = subprocess.Popen(ping_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = ping_process.communicate()
    
    print("Ping Output:", stdout.decode())
    print("Ping Errors:", stderr.decode())
    
    # Perform UDP uplink test
    print('i will start the uplink udp')
    udp_uplink_result = subprocess.run(['iperf', '-c', server.IP(), '-u'], capture_output=True, text=True)
    
    # Perform UDP downlink test
    print('i will start the downlink udp')
    udp_downlink_result = subprocess.run(['iperf', '-c', server.IP(), '-u', '-R'], capture_output=True, text=True)
    
    # Perform TCP uplink test
    print('i will start the uplink tcp')
    tcp_uplink_result = subprocess.run(['iperf', '-c', server.IP()], capture_output=True, text=True)
    
    # Perform TCP downlink test
    print('i will start the downlink tcp')
    tcp_downlink_result = subprocess.run(['iperf', '-c', server.IP(), '-R'], capture_output=True, text=True)
    
    # Perform ping test
    print('i will start the ping')
    ping_result = subprocess.run(['ping', '-c', '5', server.IP()], capture_output=True, text=True)

    # Store the results in a CSV file
    with open('results2.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([experiment_id, udp_uplink_result.stdout, udp_downlink_result.stdout, 
                         tcp_uplink_result.stdout, tcp_downlink_result.stdout, ping_result.stdout])


def main():
    if len(sys.argv) < 2:
        print("Error: No input provided.")
        sys.exit(1)
    print('le nombre de parametres:', len(sys.argv))
    input_line = sys.argv
    parameters = input_line
    print('les parametres:', parameters)
    print('len les parametres:', len(parameters))
    if len(parameters) != 8:
        print("Error: Incorrect number of parameters provided.")
        sys.exit(1)

    server_cpu_v = float(parameters[1])
    fading_v = float(parameters[2])
    delay_v = parameters[3]
    loss_v = float(parameters[4])
    bw_v = float(parameters[5])
    client_cpu_v = float(parameters[6])
    myNetwork(server_cpu_v=server_cpu_v, fading_v=fading_v, delay_v=delay_v,
              loss_v=loss_v, bw_v=bw_v, client_cpu_v=client_cpu_v)

if __name__ == '__main__':
    main()

