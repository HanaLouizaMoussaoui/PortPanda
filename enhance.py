def enhance_scan_results(scan_results):
    port_info = {
        22: "SSH (Secure Shell). Commonly used for security remote login.",
        80: "HTTP (HyperText Transfer Protocol). Used for regular web traffic.",
        443: "HTTPS (HyperText Transfer Protocol Secure). Used by encrypted web traffic."
    }

    protocol_info = {
        'tcp': "TCP is reliable and connection-oriented and used for data transfer so as to not lose any data.",
        'udp': "UDP is connectionless and is often used for real-time applications such as streaming a Youtube video."
    }

    enhanced_results = {}
    for host, results in scan_results.items():
        enhanced_results[host] = []
        for result in results:
            port = result.get('port', 'Unknown') #shows unknown if does not match
            protocol = result.get('protocol', 'Unknown').lower()
            result['description'] = port_info.get(port, "No additional information available.")
            result['protocol_info'] = protocol_info.get(protocol, "Unknown protocol.")
            enhanced_results[host].append(result)

    return enhanced_results