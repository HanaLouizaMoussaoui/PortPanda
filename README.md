# PortPanda

_Made by Taryn Beaupre, Ryan Wiwcharyk and Hana Moussaoui._

A simple port scanner with a web interface. Final project for Security course at John Abbott Cegep.


## Routes

```/```: homepage

```/scan```: sets off a scan based on the target, ports and args specified in the request


## Development Set-up Guide

Open a terminal in the project and run the following command:
```pip install -r .\requirements.txt```

Check that flask and nmap have been installed: 
```pip show flask``` and ```nmap -v```.
You may need to download nmap on your device and add it to your PATH.

To run the application, navigate to the directory containing app.py: 
```..\PortPanda> python app.py```
