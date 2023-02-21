# stromer_domoticz_plugin
A plugin for integrating Stromer EBikes into Domoticz. It will add several counters to this Domotica System.

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
