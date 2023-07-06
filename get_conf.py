from napalm import get_network_driver

# Use the appropriate network driver to connect to the device:
driver = get_network_driver('ios')

# Connect:
device = driver(
    hostname="10.1.100.3",
    username="dnauser",
    password="BvsTv3965!",
    optional_args={"port": 22},
)

device.open()

facts = device.get_facts()
print(device.get_facts())
print ('\n Hostname: ', facts['hostname'], '\n')

interfaces = device.get_interfaces()
print(interfaces)
print('\n GigabitEthernet0/0 is up: ', interfaces['GigabitEthernet0/0']['is_up'], '\n')

interfaces_counters = device.get_interfaces_counters()
print(device.get_interfaces_counters())
print ('\n GigabitEthernet0/0 TX / RX: ', interfaces_counters['GigabitEthernet0/0']['tx_unicast_packets'], ' / ', interfaces_counters['GigabitEthernet0/0']['rx_unicast_packets'],'\n')

interfaces_ip = device.get_interfaces_ip()
print(device.get_interfaces_ip())
print ('\n GigabitEthernet0/0.3004 IP Address: ', interfaces_ip['GigabitEthernet0/0.3004']['ipv4'], '\n')


