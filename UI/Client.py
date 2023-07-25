import requests


# HTTP client communicating with the cloud
class Client:
    def __init__(self):
        self.base_url = "http://[2600:1f18:61c5:5b01:9598:2ed:a6a8:fc4f]:5000"

    # Update the model (read new DB entries)
    def get_all(self, id):
        response = requests.get(f"{self.base_url}/cloud/read/{id}")
        data_arr = []
        max_id = id

        if response.status_code == 200:
            data = response.json()
            data_arr = []
            max_id = id
            for d in data:
                data_arr.append(
                    (d["ID"], d["Date"], d["Time"], int(d["Celsius"]), int(d["Scale"]))
                )
            if len(data_arr) > 0:
                max_id = data_arr[len(data_arr) - 1][0]
        else:
            print(f"Request failed with status code {response.status_code}")

        return max_id, data_arr

    # Send temperature request to the sensor node via the cloud
    def request(self):
        response = requests.get(f"{self.base_url}/cloud/request")
        if response.status_code == 200:
            data = response.json()
            return data["result"]
        else:
            print(f"Request failed with status code {response.status_code}")

