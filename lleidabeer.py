import notifications as n
import brewery as b
import time
import yaml
import pprint
import click



class LleidaBeer(object):

    """LLeidaBeer main class
    LleidaBeer is a digital, raspberry pi controlled brewery"""
    def __init__(self,fitxer="lleidabeer.yaml"):
        super(LleidaBeer, self).__init__()
        self._get_configuration(fitxer)
        self.notification_list = []
        notification = n.Notification("This is  the start test", 1)
        self.notification_list.append(notification)
        self.cmd_list = {}
        self._create_sensors()
        self._create_activeElements()
        self.channel = n.TelegramChannel(self.cfg["Telegram"]["Token"],
                                         self.cfg["Telegram"]["Users"],
                                         self.cmd_list)

    def _create_sensor_type(self, sensor_type, sensor_classes ):
        for ts in self.cfg['Sensors'][sensor_type]:

            if isinstance(ts, dict):
                name = list(ts.keys())[0]
                attri = ts[name]
            else:
                name = ts
                attri = dict()
            attri["factory"] = self
            if isinstance(sensor_classes, dict):
                sensor_class = sensor_classes[attri["type"]]
            else:
                sensor_class = sensor_classes
            self.sensor_list.append(sensor_class(name=name, **attri))


    def _create_sensors(self):
        # Create Sensors
        self.sensor_list = []
        stype = {
            "Temperature":
                {
                    "dht11": b.TemperatureSensor,
                    "mqtt": b.MQTTTemperatureSensor,
                },
            "FlowMeter": b.FlowSensor,
            'CO2Meter': b.CO2Sensor,
        }
        for k in stype:
            self._create_sensor_type(k, stype[k])

    def _create_activeElement_type(self, activeElement_type, element_class ):
        for ts in self.cfg['ActiveElements'][activeElement_type]:
            if isinstance(ts, dict):
                name = list(ts.keys())[0]
                attri = ts[name]
                
            else:
                name = ts
                attri = dict()
            attri["factory"] = self
            self.activeElement_list.append(element_class(name=name, **attri))


    def _create_activeElements(self):
        # Create Active Elements
        self.activeElement_list = []
        stype = {
            "Mixer": b.Mixer,
            "Heater": b.Heater,
            "MQTTMixer": b.MQTTMixer,
            "MQTTHeater": b.MQTTHeater,
        }
        for k in stype:
            self._create_activeElement_type(k, stype[k])

    # FIXME: subcmd shouldn't be none or deal with none
    # IDEA: instead of subcmd as string, deal with subcmd as list
    def register_command(self, cmdtext, cmdfunction, subcmd = None ):
        # TODO: All commands to lowercase
        cmdtext = cmdtext.lower()
        print("DEBUG "+cmdtext+"*"+subcmd)
        if cmdtext not in self.cmd_list:
            self.cmd_list[cmdtext] = dict()
        if subcmd not in self.cmd_list[cmdtext]:
            self.cmd_list[cmdtext][subcmd] = list()
        self.cmd_list[cmdtext][subcmd].append(cmdfunction)

    def _get_configuration(self,config):
  
        name = config
        with open(name,"r") as f:
            self.cfg = yaml.load(f)
        pprint.pprint(self.cfg)
        
   
    def main(self):
            while True:
                # Update Sensor Readings
                for sensor in self.sensor_list:
                    sensor.update_value()
                       
                    

                for sensor in self.sensor_list:
                    if sensor.has_alarm():
                        notification = n.Notification("Alarm: The "+sensor.name+
                                                      " Temperature sensor exceeds "
                                                      +str(sensor.value)+" ºC",1)
                        self.notification_list.append(notification)
                        
                # Command processing
                #
                # Notifications
                while len(self.notification_list)>0:
                    notification = self.notification_list.pop()
                    self.channel.send_notification(notification)
                time.sleep(5)

@click.command()
@click.option('--config', default='lleidabeer.yaml', help='Name of the configuration yaml')
def main(config):
    lleidabeer = LleidaBeer(config)
    lleidabeer.main()


if __name__ == "__main__":
    main()
