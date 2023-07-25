import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import json
from flask import Flask, jsonify
from flask_cors import CORS


# Create a database connection and cursor
conn = sqlite3.connect("mybase")
cursor = conn.cursor()

# MQTT broker settings
broker_address = "2600:1f18:61c5:5b01:9598:2ed:a6a8:fc4f"
broker_port = 1886
topic = "mytopic/temp1"
topic_r = "mytopic/request1"


# Handle receiving temperature messages
def on_message(client, userdata, msg):
    # Extract the received data
    data_str = msg.payload.decode()
    result = data_str.split(",")
    value = int(result[0])
    scale = int(result[1])

    # Get date and time and store as string
    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%d.%m.%Y")
    time_string = current_datetime.strftime("%H:%M:%S")
    conn = sqlite3.connect("mybase")
    cursor = conn.cursor()

    # Store the received data in the database
    cursor.execute(
        "INSERT INTO temperature (date, time, value, scale) VALUES (?, ?, ?, ?)",
        (date_string, time_string, value, scale),
    )
    conn.commit()
    conn.close()


# Create an MQTT client
client = mqtt.Client(client_id="MQTT_Client")
client.on_message = on_message
try:
    client.connect(broker_address, port=broker_port, keepalive=60)
    client.subscribe(topic)
except:
    print("Could not connect to broker")
    exit()


# Start MQTT client loop
client.loop_start()


# ---HTTP Server---

app = Flask(__name__)
CORS(app)


# Send DB data to UI
@app.route("/cloud/read/<param>", methods=["GET"])
def read_data(param):
    conn = sqlite3.connect("mybase")
    cursor = conn.cursor()
    last_id = int(param)
    cursor.execute(
        "SELECT * FROM temperature where id > ?;",
        (last_id,),
    )
    rows = cursor.fetchall()
    temperature_data = []
    for row in rows:
        x = int(row[3])
        y = int(row[4])
        # Create a dictionary for each row of data
        data = {
            "ID": row[0],
            "Date": row[1],
            "Time": row[2],
            "Celsius": row[3],
            "Scale": row[4],
        }
        # Append the dictionary to the list
        temperature_data.append(data)
    # Convert the temperature list to JSON
    json_data = json.dumps(temperature_data)
    return json_data


# Send rqeuest to sensor node
@app.route("/cloud/request", methods=["GET"])
def request_data():
    print("Requesting data")
    message = "get_temp_now"
    try:
        client.publish(topic_r, message)
        return jsonify({"result": "Data requested"})
    except:
        return jsonify({"result": "Could not reach the sensor node"})


if __name__ == "__main__":
    app.run(host="::", port=5000)

# Close MQTT Client and DB Connection
client.loop_stop()
client.disconnect()
conn.close()
