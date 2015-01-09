from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
red = redis.StrictRedis(host='localhost', port=6379, db=0)

# Helper functions
def saveMessage(msg):
  new_id = red.incr('messageid')
  red.hset('messages', new_id, msg.rstrip()) # chomp whitespace, e.g. '\n'
  return jsonify(message_id=new_id, message_content=msg)

def getMessage(mid):
  if red.hexists('messages', mid):
    return red.hget('messages', mid)

  return 'no such message', 404

# Routing functions
# Input route - data is posted and we save it
@app.route("/in/", methods=['POST'])
def inRoute():
  message = request.data if request.data else request.form.keys().pop()
  if message:
    return saveMessage(message)

  return 'No data received', 400


# Output route - output message identified by mid
@app.route('/messages/<int:mid>/')
def outRoute(mid):
  return getMessage(mid)


# Ensure the server only runs from Python interpreter and not if used as an
# imported module
if __name__ == '__main__':
  app.debug = True # using for the livereload functionality
  app.run(
    port=8888
  )
