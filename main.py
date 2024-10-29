from flask import Flask, render_template, request, jsonify
import paho.mqtt.publish as publish
import ssl

app = Flask(__name__)

# MQTT Broker details
broker = "broker.emqx.io"  # Replace with your actual broker URL, e.g., "47d17e0eec0047ef9a75d70c3672d310.s2.eu.hivemq.cloud"
port = 1883  # Secure port for TLS/SSL connection
username = "emqx"  # Replace with your HiveMQ Cloud username
password = "public"  # Replace with your HiveMQ Cloud password
topic = "noobyco"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post_data():
    data = request.get_json()
    direction = data.get('signal', '')
    print(f'Received direction: {direction}')  
    publish.single(
        topic=topic,
        payload=direction,
        hostname=broker,
        port=port,
        auth={'username': username, 'password': password},
        keepalive=60  # Increase keepalive if needed
    )
    print(f"Message '{direction}' published to topic '{topic}'")
    return jsonify({"status": "Message published", "direction": direction})

if __name__ == '__main__':
    app.run(debug=True)

