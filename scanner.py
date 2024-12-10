import socket
import ssl
import threading
import nmap
import json
import subprocess
import ipaddress

results = {}

def scan_udp_ports(host, port):
    nm = nmap.PortScanner()
    try:
        # Perform a UDP scan on the specified ports
        nm.scan(hosts=host, ports=port, arguments='-sU')
        for port in nm[host]['udp']:
            state = nm[host]['udp'][port]['state']
            service = nm[host]['udp'][port]['name']
            results[host].append(
                {
                    "port": port,
                    "protocol": "udp",
                    "state": state,
                    "service": service if service else "Unknown"
                }
            )
    except Exception as e:
        results[host].append({
            "port": port,
            "protocol": "udp",
            "error": str(e)
        })

def scan_port(host, port, protocol):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if protocol.lower() == 'udp':
            scan_udp_ports(host, str(port))
        elif protocol.lower() == 'tcp':
            use_ssl = port == 443
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, protocol.lower())
                except OSError:
                    service = "Unknown service"
                service_ver = grab_serv_version(sock, use_ssl)
                results[host].append({
                    "port": port,
                    "protocol": "tcp",
                    "state": "open",
                    "service": service,
                    "banner": service_ver
                })
            else:
                results[host].append({
                    "port": port,
                    "protocol": "tcp",
                    "state": "closed"
                })
        else:
            results[host].append({
                "port": port,
                "protocol": protocol,
                "error": "Unsupported protocol"
            })
        sock.close()
    except Exception as e:
        results[host].append({
            "port": port,
            "protocol": protocol,
            "error": str(e)
        })

def scan_range(hosts, ports, protocol='tcp'):
    for host in hosts:
        if not is_valid_ipv4_address(host):
            host = socket.gethostbyname(host)
        host_ip = socket.gethostbyname(host)
        results[host] = []
        threads = []

        if isinstance(ports, str):
            start_port, end_port = map(int, ports.split('-'))
            ports = range(start_port, end_port + 1)
        elif isinstance(ports, int):
            ports = [ports]

        for port in ports:
            thread = threading.Thread(target=scan_port, args=(host_ip, port, protocol))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        reverse_dns_result = reverse_dns_lookup(host_ip)
        if isinstance(reverse_dns_result, Exception):
            hostname = "Unknown hostname"
        else:
            hostname, aliases = reverse_dns_result

        print(f"Scan results for {hostname} ({host}) on transport protocol {protocol.upper()}")
        results[host].append(get_target_os(host))

        if len(ports) == 1:
            total_ports = 1
        else:
            total_ports = end_port - start_port + 1

        open_ports = sum(1 for result in results.get(host, []) if isinstance(result, dict) and "open" in result.get("state", ""))
        
        results[host].append({
            "total_ports_scanned": total_ports,
            "open_ports": open_ports,
            "closed_ports": total_ports - open_ports,
            "hostname": hostname})
        #print(json.dumps(results[host], indent=2))
    return results


def grab_serv_version(sock, use_ssl=False):
    try:
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname="localhost")
        sock.send(b'HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n')
        banner = sock.recv(1024).decode().strip()
        if not banner:
            sock.send(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
            banner = sock.recv(1024).decode().strip()
        return banner
    except Exception as e:
        return f"Error grabbing banner: {e}"

def get_target_os(target):
    nm = nmap.PortScanner()

    try:
        results = nm.scan(target, arguments='-O')
        os_info = {}
        if 'osmatch' in results['scan'][target]:
            os_match = results['scan'][target]['osmatch'][0]
            os_info['os_name'] = os_match['name']
            os_info['os_accuracy'] = os_match['accuracy']
        if 'tcp' in results['scan'][target]:
            os_info['open_ports'] = list(results['scan'][target]['tcp'].keys())
            os_info['services'] = {port: results['scan'][target]['tcp'][port]['name'] for port in os_info['open_ports']}
        return os_info
    except Exception as e:
        return f"Error detecting OS: {e}"

def reverse_dns_lookup(ip):
    try:
        hostname, aliases, _ = socket.gethostbyaddr(ip)
        return hostname, aliases
    except Exception as e:
        return e
    

def is_valid_ipv4_address(address):
    try:
        ip = ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False
