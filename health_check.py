import requests

try:
    response = requests.get("http://localhost:30000/health")
    if response.status_code == 200:
        print("Health check passed")
        exit(0)
    else:
        print("Health check failed")
        exit(1)
except requests.exceptions.RequestException as e:
    print(f"Health check error: {e}")
    exit(1)
