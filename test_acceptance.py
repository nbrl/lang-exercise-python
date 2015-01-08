import unittest
import langapp
import redis
import flask
import json

class LangAppPostingMessages(unittest.TestCase):
  def setUp(self):
    red = redis.StrictRedis('localhost', 6379, db=0)
    red.delete('messages')
    red.delete('messageid')
    self.app = langapp.app.test_client()

  def tearDown(self):
    pass

  def test_post_good_message(self):
    message = 'hello there'
    post_data = dict([(message, u'')])
    rv = self.app.post('/in/', data=post_data)
    json_data = json.loads(rv.data)
    expected = {
        'message_content': message,
        'message_id': 1
    }
    self.assertEqual(rv.status_code, 200)
    self.assertEqual(json_data, expected)

  def test_post_empty_message(self):
    rv = self.app.post('/in/', data=None)
    self.assertEqual(rv.status_code, 400)
    self.assertEqual(rv.data, 'No data received')

class LangAppReadingMessages(unittest.TestCase):
  def setUp(self):
    red = redis.StrictRedis('localhost', 6379, db=0)
    red.delete('messages')
    red.delete('messageid')
    for i in range(0, 3):
      n = red.incr('messageid')
      red.hset('messages', i, 'message number ' + str(i))
    self.app = langapp.app.test_client()

  def tearDown(self):
    pass

  def test_retrieve_message(self):
    rv = self.app.get('/messages/0/')
    self.assertEqual(rv.status_code, 200)
    self.assertEqual(rv.data, 'message number 0')
    rv = self.app.get('/messages/1/')
    self.assertEqual(rv.status_code, 200)
    self.assertEqual(rv.data, 'message number 1')
    rv = self.app.get('/messages/2/')
    self.assertEqual(rv.status_code, 200)
    self.assertEqual(rv.data, 'message number 2')

  def test_retrieve_non_exist_message(self):
    mid = '12345'
    rv = self.app.get('/messages/' + mid + '/')
    self.assertEqual(rv.data, 'no such message')
    self.assertEqual(rv.status_code, 404)

  def test_retreive_non_int_id(self):
    mid = 'abc'
    rv = self.app.get('/messages/' + mid + '/')
    self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
  unittest.main()
