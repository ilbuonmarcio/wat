from liquidctl import find_liquidctl_devices
from pprint import pprint
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='wat',
                             password='123',
                             database='wat',
                             cursorclass=pymysql.cursors.DictCursor)

devices = find_liquidctl_devices()

for dev in devices:
    if dev._description != 'Corsair HX1000i':
        continue
    
    with dev.connect():
        print(f'{dev.description} at {dev.bus}:{dev.address}:')
        init_status = dev.initialize()

        status = dev.get_status()
        values = {
            "output": None,
            "input": None,
            "efficiency": None,
            "fan_speed": None,
            "case_temperature": None,
            "vrm_temperature": None
        }
        
        for key, value, unit in status:
            if key == "VRM temperature":
                values["vrm_temperature"] = value
            elif key == "Case temperature":
                values["case_temperature"] = value
            elif key == "Fan speed":
                values["fan_speed"] = value
            elif key == "Total power output":
                values["output"] = value
            elif key == "Estimated input power":
                values["input"] = value
            elif key == "Estimated efficiency":
                values["efficiency"] = value

        pprint(values)

        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `logs` (`input`, `output`, `efficiency`, `fan_speed`, `case_temperature`, `vrm_temperature`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (
                    values['input'],
                    values['output'],
                    values['efficiency'],
                    values['fan_speed'],
                    values['case_temperature'],
                    values['vrm_temperature']
                ))

            connection.commit()