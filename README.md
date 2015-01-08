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

## Saving new dependencies
If the dependencies for the project change, update the requirements.
```bash
pip freeze > requirements.txt
```
