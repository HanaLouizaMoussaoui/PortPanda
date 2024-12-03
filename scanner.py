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
def scan_port(host, port):
    try:
        use_ssl = port == 443
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(1)
        # Attempt to connect to the host and port
        result = sock.connect_ex((host, port))
        # If the connection was successful, the port is open
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown service"
            service_ver = grab_serv_version(sock, use_ssl)
            print(f"Port {port} is open (Service: {service}, Banner: {service_ver})")
        else:
            print(f"Port {port} is closed")
        # Close the socket
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Function to scan a range of ports
def scan_range(host, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        # Create a new thread for each port scan
        thread = threading.Thread(target=scan_port, args=(host, port))
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


# Main function
if __name__ == "__main__":
    target_host = socket.gethostbyname('www.megacorpone.com')  # Target IP address
    start_port = 1  # Starting port number
    end_port = 1000  # Ending port number
    scan_range(target_host, start_port, end_port)
    print(get_target_os(target_host))