from flask import Flask, request, jsonify, render_template
import nmap
import socket
from flask import Flask, jsonify
from scanner import scan_range, scan_port, get_target_os
from enhance import enhance_scan_results

import threading

app = Flask(__name__)
scanner = nmap.PortScanner()


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/results")
def results():
    return render_template('results.html')


@app.route("/scan", methods=['POST'])
def scan():
    try:
        protocol = request.form.get('protocol', 'tcp').lower()  # default is tcp
        start_port = request.form.get('start_port', '1')  # default is 1
        end_port = request.form.get('end_port', '500')  # default is the max (65535)
        single_port = request.form.get('single_port', False)  # if user wants to scan only one port
        ip_range = request.form.get('ip_range', 'www.megacorpone.com')

        # validating port inputs
        if not start_port.strip().isdigit():
            start_port = 1
        else:
            start_port = int(start_port)

        if not end_port.strip().isdigit():
            end_port = 500  # default
        else:
            end_port = int(end_port)

        hosts_list = ip_range.split(',')

        if single_port:
            ports = end_port
        else:
            # making sure the port range entered is valid
            if start_port < 1 or start_port > 65534:
                return render_template('error.html', error="Start port must be between 1 and 65534."), 400
            if end_port < 2 or end_port > 65535:
                return render_template('error.html', error="End port must be between 2 and 65535."), 400
            if start_port > end_port:
                return render_template('error.html', error="Start port cannot be greater than end port."), 400
            ports = f"{start_port}-{end_port}"

        results = scan_range(hosts_list, ports, protocol)
        open_ports_results = {}
        for host, host_results in results.items():
            open_ports_results[host] = [result for result in host_results if
                                        isinstance(result, dict) and 'open' in result.get('state', '')]
            os, accuracy = get_os_name_from_results(host_results)
            open_ports_results[host].append({
                "os_name": os,
                "os_accuracy": accuracy

            })
            open_ports_results[host].append({
                "closed_ports": get_closed_ports(host_results)
            })

        enhanced_results = enhance_scan_results(open_ports_results)  # appends educational content to the results.
        print("ENHANCED: ", enhanced_results)
        return render_template('results.html', results=enhanced_results)  # returning the results as a json object

    except Exception as e:
        return render_template('error.html', error=f"Exception {e} was thrown."), 500

def get_os_name_from_results(scan_results):
    for result in scan_results:
        if isinstance(result, dict) and 'os_name' in result:
            return result['os_name'], result['os_accuracy']

def get_closed_ports(scan_results):
     for result in scan_results:
         if isinstance(result, dict) and 'closed_ports' in result:
             return result['closed_ports']

if __name__ == '__main__':
    app.run(debug=True)