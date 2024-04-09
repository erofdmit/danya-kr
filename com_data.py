import random
import requests
for i in range(100):
    detector_id = random.randint(1, 12)
    value = random.random() * 1000
    input_data = {'detector_id' : detector_id, 'value' : value}
    requests.post(url='http://localhost:8000/api/input/put_detector_data', json=input_data)