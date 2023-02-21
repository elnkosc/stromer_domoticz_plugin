# Domoticz Stromer EBike Plugin
#
# Author: Koen Schilders
#
"""
<plugin key="StromerEBike" name="Stromer EBike Plugin" author="Koen Schilders" version="1.0.0" externallink="https://github.com/elnkosc/stromer_api">
    <description>
        <h2>Stromer EBike Integration</h2><br/>
        Will obtain data from the Stromer Portal once every 30 heartbeats (5 minutes).
    </description>
    <params>
        <param field="Username" label="Username" required="true" width="200px"/>
        <param field="Password" label="Password" required="true" width="200px" password="true"/>
        <param field="Mode1" label="Client ID" required="true" width="200px"/>
    </params>
</plugin>
"""
import DomoticzEx as Domoticz
from stromer_api import StromerBike

class StromerEBikePlugin:
    def __init__(self):
        self.__update_freq_sec = 3600
        self.__update_counter = 0
        self.__domoticz_heartbeat_sec = 15
        self.__bike = None
        return

    def onStart(self):
        Domoticz.Log("Stromer EBike Started")
        DumpConfigToLog()
        Domoticz.Heartbeat(self.__domoticz_heartbeat_sec)

        try:
            self.__bike = StromerBike(Parameters["Username"], Parameters["Password"], Parameters["Mode1"])
            
            if not "Battery Health" in Devices:
                Domoticz.Unit(Name="Battery Health", DeviceID="Battery Health", Unit=1, TypeName="Percentage").Create()

            if not "Distance" in Devices:
                Domoticz.Unit(Name="Distance", DeviceID="Distance", Unit=1, TypeName="Distance").Create()

            if not "Average Distance" in Devices:
                Domoticz.Unit(Name="Average Distance", DeviceID="Average Distance", Unit=1, TypeName="Distance").Create()

            if not "Trip Distance" in Devices:
                Domoticz.Unit(Name="Trip Distance", DeviceID="Trip Distance", Unit=1, TypeName="Distance").Create()

            if not "Total Energy Consumption" in Devices:
                Domoticz.Unit(Name="Total Energy Consumption", DeviceID="Total Energy Consumption", Unit=1, TypeName="kWh").Create()

            if not "Average Energy Consumption" in Devices:
                Domoticz.Unit(Name="Average Energy Consumption", DeviceID="Average Energy Consumption", Unit=1, TypeName="kWh").Create()

            if not "Total Time" in Devices:
                Domoticz.Unit(Name="Total Time", DeviceID="Total Time", Unit=1, TypeName="Custom").Create()

        except:
            Domoticz.Log("Stromer EBike Plugin: could not connect to Stromer Portal")

    def onStop(self):
        Domoticz.Log("Stromer EBike Stopped")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, DeviceID, Unit, Command, Level, Color):
        Domoticz.Log("onCommand called for Device " + str(DeviceID) + " Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        self.__update_counter += 1
        if self.__update_counter * self.__domoticz_heartbeat_sec >= self.__update_freq_sec:
            self.__update_counter = 0
            self.__bike.refresh()
            
            # check if re-connect is needed
            if self.__bike.state is None:
                self.__bike = StromerBike(Parameters["Username"], Parameters["Password"], Parameters["Mode1"])

            Devices["Battery Health"].Units[1].nValue = 0
            Devices["Battery Health"].Units[1].sValue = str(self.__bike.state.battery_health)
            Devices["Battery Health"].Units[1].Update(Log=True)

            Devices["Distance"].Units[1].nValue = 0
            Devices["Distance"].Units[1].sValue = "{dist:.2f}".format(dist=self.__bike.statistics.total_km)
            Devices["Distance"].Units[1].Update(Log=True)

            Devices["Average Distance"].Units[1].nValue = 0
            Devices["Average Distance"].Units[1].sValue = "{dist:.2f}".format(dist=self.__bike.statistics.average_km)
            Devices["Average Distance"].Units[1].Update(Log=True)

            Devices["Trip Distance"].Units[1].nValue = 0
            Devices["Trip Distance"].Units[1].sValue = "{dist:.2f}".format(dist=self.__bike.state.trip_distance)
            Devices["Trip Distance"].Units[1].Update(Log=True)

            Devices["Total Energy Consumption"].Units[1].nValue = 0
            Devices["Total Energy Consumption"].Units[1].sValue = "0;" + str(self.__bike.statistics.total_wh)
            Devices["Total Energy Consumption"].Units[1].Update(Log=True)
       
            Devices["Average Energy Consumption"].Units[1].nValue = 0
            Devices["Average Energy Consumption"].Units[1].sValue = "0;" + str(self.__bike.statistics.average_wh)
            Devices["Average Energy Consumption"].Units[1].Update(Log=True)
       
            Devices["Total Time"].Units[1].nValue = 0
            Devices["Total Time"].Units[1].sValue = "{dist:.0f}".format(dist=self.__bike.statistics.total_sec)
            Devices["Total Time"].Units[1].Update(Log=True)


global _plugin
_plugin = StromerEBikePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(DeviceID, Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(DeviceID, Unit, Command, Level, Color)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for DeviceName in Devices:
        Device = Devices[DeviceName]
        Domoticz.Debug("Device ID:       '" + str(Device.DeviceID) + "'")
        Domoticz.Debug("--->Unit Count:      '" + str(len(Device.Units)) + "'")
        for UnitNo in Device.Units:
            Unit = Device.Units[UnitNo]
            Domoticz.Debug("--->Unit:           " + str(UnitNo))
            Domoticz.Debug("--->Unit Name:     '" + Unit.Name + "'")
            Domoticz.Debug("--->Unit nValue:    " + str(Unit.nValue))
            Domoticz.Debug("--->Unit sValue:   '" + Unit.sValue + "'")
            Domoticz.Debug("--->Unit LastLevel: " + str(Unit.LastLevel))
    return
