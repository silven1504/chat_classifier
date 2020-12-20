import json
import base64
import os

from json import dumps

with open('test_data.txt', 'r') as fin:
    data = fin.readlines()

jsarray = json.dumps(data)
urlSafeEncodedBytes = base64.urlsafe_b64encode(jsarray.encode("utf-8"))
urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")

print('Predict labels for data:')
print(data)
os.system(f'curl localhost:8080/predict?input={urlSafeEncodedStr}')
print('')

print(f'Probability:')
os.system(f'curl localhost:8080/predict_proba?input={urlSafeEncodedStr}')
