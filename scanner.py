import socket
import ssl
import threading
import nmap


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

# Function to scan a single port
# protocol will be obtained from form data on flask site
def scan_port(host, port, protocol):
    try:
        if protocol.lower() == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # use https if port is 443: https port
        use_ssl = port == 443
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        # If the connection was successful, the port is open
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown service"
            if protocol.lower() == 'tcp':
                service_ver = grab_serv_version(sock, use_ssl)
                print(f"Port {port} ({protocol}) is open (Service: {service}, Banner: {service_ver})")
            else:
                if service.lower() == "unknown service":
                    print(f"Port {port} ({protocol}) is open (Service: {service} or the port is unresponsive)")
        else:
            print(f"Port {port} ({protocol}) is closed")
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Function to scan a range of ports
def scan_range(host, start_port, end_port, protocol='tcp'):
    threads = []
    for port in range(start_port, end_port + 1):
        # Create a new thread for each port scan
        thread = threading.Thread(target=scan_port, args=(host, port, protocol))
        threads.append(thread)
        thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

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


if __name__ == "__main__":
    target_host = socket.gethostbyname('www.megacorpone.com')
    start_port = 1
    end_port = 1000
    scan_range(target_host, start_port, end_port, protocol='tcp')
    scan_range(target_host, start_port, end_port, protocol='udp')
    print(get_target_os(target_host))