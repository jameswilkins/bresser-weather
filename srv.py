from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

app = Flask(__name__)


# InfluxDB configuration
INFLUXDB_URL = os.environ.get('INFLUXDB_URL','http://localhost:8096')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', 'your-default-token')
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG', 'your-default-org')
INFLUXDB_BUCKET = os.environ.get('INFLUXDB_BUCKET', 'your-default-bucket')

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test InfluxDB connection by fetching the list of buckets
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets().buckets
        influxdb_status = 'connected' if buckets is not None else 'disconnected'
    except Exception as e:
        influxdb_status = f'error: {str(e)}'

    return jsonify({"status": "success", "message": "Application is running", "influxdb": influxdb_status}), 200

@app.route('/weatherstation/updateweatherstation.php', methods=['GET'])
def update_data():
    # Extracting parameters from the query string
    data = {key: request.args.get(key) for key in request.args}

    # Convert parameters to InfluxDB Point (modify field names as needed)
    point = Point("weather_data").tag("location", "default")
    for key, value in data.items():
        point = point.field(key, float(value) if value.replace('.', '', 1).isdigit() else value)

    # Write point to InfluxDB
    write_api.write(bucket=INFLUXDB_BUCKET, record=point)

    # Return a response
    return jsonify({"message": "Data received and written to InfluxDB", "received_data": data})

if __name__ == '__main__':
    app.run(debug=True, port=30000,host='0.0.0.0')
