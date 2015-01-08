import unittest
import langapp
import mock
import redis

class LangAppPostMessage(unittest.TestCase):

  def setUp(self):
    # Runs for every test
    self.app = langapp.app.test_client()

    # Patch redis so it doesn't connect to the real one
    self.redisPatcher = mock.patch('langapp.red')
    self.mockRedis = self.redisPatcher.start()

  def tearDown(self):
    self.redisPatcher.stop()
    pass

  def test_check_test_env_is_sane(self):
    assert langapp.red is self.mockRedis

  #def test_new_message_increments(self):
  #  real_redis = langapp.red
  #  real_redis.incr = mock.MagicMock(name='incr')
  #  self.app.post('/in/', data='doesnt matter')
  #  real_redis.incr.assert_called_once_with('messageid')

  @mock.patch('langapp.red.incr')
  def test_new_message_increments(self, redis_incr):
    redis_incr.return_value = 1
    self.app.post('/in/', data='doesnt matter')
    redis_incr.assert_called_once_with('messageid')

  @mock.patch('langapp.red.hset')
  def test_new_message_added_to_hash(self, redis_hset):
    self.app.post('/in/', data='some data')
    redis_hset.assert_called_once_with('messages', 1, 'some data')

if __name__ == '__main__':
  unittest.main(verbosity = 2)
