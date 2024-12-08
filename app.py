from flask import Flask, request, jsonify, render_template
import nmap
import socket
from flask import Flask, jsonify
import threading

app = Flask(__name__)
# scanner = nmap.PortScanner()


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/scan", methods=['POST'])
def scan():
    data = request.json
    target = data.get('target', '127.0.0.1') # target IP
    ports = data.get('ports', '22-80') #the ports to be scanned
    args = data.get('args', '-sS') #the scan type and arguments

    try:
        results = scanner.scan(hosts=target, ports=ports, arguments=args) #using nmap library to configure the scan
        return jsonify(results) #returning the results as a json object
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)