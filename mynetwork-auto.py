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
import subprocess
import csv

def myNetwork(server_cpu_v=1,fading_v=3,delay_v='0ms',loss_v=0,bw_v=10,client_cpu_v=1,experiment_id=None):

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
    server = net.addHost('server', cls=Host, ip='10.0.0.2', defaultRoute=None, cpu=server_cpu_v)
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='480.0,241.0,0', cpu=client_cpu_v) 

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=fading_v)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')
    net.addLink(server, ap1 ,loss=loss_v,delay=delay_v,bw=bw_v)

    net.plotGraph(max_x=1000, max_y=1000)

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

 

    # Start the iperf server on 'server' host
    info('*** Configuring Nginx on the server\n')
    # Configure Nginx using the specified config file. Adjust the path as necessary.
    server.cmd('nginx -c /home/sghandi/Téléchargements/wemon-main/nginx-conf.conf')

# Test the Nginx configuration
    server.cmd('nginx -t')

# Instead of using systemctl to reload Nginx, directly restart Nginx
# This is necessary because systemctl commands may not work as expected in Mininet's simulated environments
    server.cmd('nginx -s reload') # or 'nginx -s stop' followed by 'nginx'

    time.sleep(1) 
    
    print('i configured nginx')    
    
    #server.cmd('iperf -s &')
    
    #CLI(net)
    #net.stop()
    print('i stopped mininet ')
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
    print('i will start the downlink udp')
    tcp_downlink_result = subprocess.run(['iperf', '-c', server.IP(), '-R'], capture_output=True, text=True)
    
    # Perform ping test
    print('i will start the ping')
    ping_result = subprocess.run(['ping', '-c', '5', server.IP()], capture_output=True, text=True)

    # Store the results in a CSV file
    with open('results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([experiment_id, udp_uplink_result.stdout, udp_downlink_result.stdout, 
                         tcp_uplink_result.stdout, tcp_downlink_result.stdout, ping_result.stdout])

def run_command(command):
    """ Run shell commands """
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(f"Command Output: {output.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.output.decode()}")

def clear_mininet_wifi():
    """ Cleanup Mininet environments """
    print("Running Mininet cleanup...")
    run_command('sudo mn -c')

def remove_and_reload_mac80211_hwsim():
    """ Remove and reload the mac80211_hwsim module """
    print("Removing mac80211_hwsim module...")
    run_command('sudo rmmod mac80211_hwsim')
    print("Reinserting mac80211_hwsim module...")
    run_command('sudo modprobe mac80211_hwsim')

def check_wifi_module():
    """ Check if the WiFi module is loaded correctly """
    print("Checking mac80211_hwsim module...")
    run_command('lsmod | grep mac80211_hwsim')



def read_parameters_from_file(file_path):
    """
    Read parameter values from the specified file.

    Parameters:
    - file_path: Path to the file containing parameter values.

    Returns:
    - A list of tuples, where each tuple contains parameter values.
    """
    parameter_tuples = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):  # Start line numbering from 1
            # Assuming parameters are space-separated in each line
            parameters = line.strip().split()
            experiment_id = line_number  # Use line number as experiment ID
            parameter_tuples.append((experiment_id, parameters))
    return parameter_tuples

if __name__ == '__main__':
    setLogLevel('info')

    # Read parameter values from the file
    parameter_tuples = read_parameters_from_file('/home/sghandi/Téléchargements/wemon-main/parameter_file1.txt')

    # Iterate over each tuple of parameter values
    for experiment_id, parameters in parameter_tuples:
        # Convert parameter values to appropriate types if necessary
        server_cpu_v = float(parameters[0])
        fading_v = float(parameters[1])
        delay_v = parameters[2]
        loss_v = float(parameters[3])
        bw_v = float(parameters[4])
        client_cpu_v = float(parameters[5])

	#net = Mininet_wifi()

        # Call myNetwork function with the current set of parameter values
        print('I am on experiment:  ',experiment_id)
        myNetwork(server_cpu_v=server_cpu_v, fading_v=fading_v, delay_v=delay_v,
                  loss_v=loss_v, bw_v=bw_v, client_cpu_v=client_cpu_v,experiment_id=experiment_id)
                  
                  
                  
                  
         # Stop and clear the existing Mininet network
        clear_mininet_wifi()
        #remove_and_reload_mac80211_hwsim()
        time.sleep(2) 
        #check_wifi_module()
        print('i cleared last mininet')
        
        clear_mininet_wifi()
        #net.stop()                 

