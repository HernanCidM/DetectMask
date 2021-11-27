import json
import random
import time

import paho.mqtt.client as mqtt


def sending_data_mqtt(peopleWithoutMask, peopleWithMask, totalPeople):
    THINGSBOARD_HOST = 'iot.ceisufro.cl'
    ACCESS_TOKEN = 'Hbu7rZWGLtTLXTFNm9Yi'

    INTERVAL = 1

    sensor_data = {'total people': totalPeople, 'people without mask': peopleWithoutMask, 'people with mask': peopleWithMask}

    next_reading = time.time()

    client = mqtt.Client()

    client.username_pw_set(ACCESS_TOKEN)

    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()
    try:
        print(u"People with mask: {:g}\u00b0C, People without mask: {:g}%, Total people: {:g}%".format(peopleWithMask, peopleWithoutMask, totalPeople))
        print(json.dumps(sensor_data))
        sensor_data['people with mask'] = peopleWithMask
        sensor_data['people without mask'] = peopleWithoutMask
        sensor_data['total people'] = totalPeople
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass

    client.loop_stop()
    client.disconnect()