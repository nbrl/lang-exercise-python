from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
red = redis.StrictRedis(host='localhost', port=6379, db=0)

# Testing route to make sure the app is running
@app.route('/')
def root():
  return 'Hello world!'

# Input root - data is posted and we save it
@app.route("/in/", methods=['POST'])
def new_message():
  new_id = red.incr('messageid')
  # Flask is weird.
  # Supported requests go to requests.form (or .values)
  # Unsupported requests go to requests.data (which is where text/plain goes)
  msg = request.form.keys().pop(0)
  red.hset('messages', new_id, msg)
  return jsonify(message_id=new_id, message_content=msg)

# Output route - output message identified by mid
@app.route('/messages/<int:mid>/')
def msg(mid):
  msg = red.hget('messages', mid)
  if msg:
    return msg
  return 'no such id: %i' % mid

# Ensure the server only runs from Python interpreter and not if used as an
# imported module
if __name__ == '__main__':
  app.debug = True # using for the livereload functionality
  app.run(
    port=8888
  )
