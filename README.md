# lang-exercise-python
Testing a simple Redis messaging server with Python

## Setup
We need a few packages installed globally for testing.
```bash
sudo pip install coverage nose
```

Then we need to set up the environment ready to run.
```bash
virtualenv env
source ./env/bin/activate
pip install -r requirements.txt
```

To exit the virtualenv use `deactivate`

## Running the app
To use Redis needs to be running (as yet no error checking if the app is started without redis):
```bash
# Install package for redis server (e.g. brew install redis)
redis-server
```

Simply:
```bash
python langapp.py
```

To send a new message:
```bash
curl http://127.0.0.1:8888/in/ -d 'your message'
```

To query a message by id:
```bash
curl http://127.0.0.1:8888/messages/<int:id>/
```

## Testing the app
To run all the tests:
```bash
nosetests test
```

## Saving new dependencies
If the dependencies for the project change, update the requirements.
```bash
pip freeze > requirements.txt
```
