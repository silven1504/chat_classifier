### ds mini-project

to built docker image do (this may take a while):
```
git clone ‘https://github.com/silven1504/chat_classifier.git’
docker build -t classifier:1.0 .
```

for starting rest-api app do
```
docker run -p 8080:8080 --name ChatClassifier classifier:1.0
```

for starting testing do
```
cd test
python3 service_test.py
```
You can also use your own data for testing. Edit test/test_data.txt for that.
