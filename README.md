# stromer_domoticz_plugin
A plugin for integrating Stromer EBikes into Domoticz. It will add several counters to this Domotica System. When adding the hardware, you have to provide the username and password for your Stromer account as well as the Client ID. This can be obtained in several ways (eg extracting it out of the Android apk file of the Stromer Mobile App, monitoring the internet connection between app and server (eg using mitmproxy), or get a hint by contacting me.

In order to use the plugin do the following when at the linux command line of your Domoticz system:
```
# install pip package manager for python3
sudo apt-get install python3-pip

# install required libraries: xsltwriter & stromer_api
sudo pip3 install xsltwriter
sudo pip3 install stromer_api

# go to the Domoticz plugin directory, create directory, and install the plugin
cd ~/domoticz/plugins
mkdir stromer-ebike
cd stromer-ebike
wget https://github.com/elnkosc/stromer_domoticz_plugin/blob/main/plugin.py

# now restart domoticz
sudo service domoticz restart
