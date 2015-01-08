import unittest
import langapp
import mock

class LangAppPostMessage(unittest.TestCase):
  def setUp(self):
    self.app = langapp.app.test_client()

  #@mock.patch('redis.StrictRedis')
  #def test_new_message_increments(self, strict_redis):
  def test_new_message_increments(self):
    #strict_redis.incr.assert_called_once_with('messageid')
    real_redis = langapp.red
    real_redis.incr = mock.MagicMock(name='incr')
    #real_redis.incr('messageid')
    #print dir(real_redis.incr)
    self.app.post('/in/', data='doesnt matter')
    real_redis.incr.assert_called_once_with('messageid')

  @mock.patch('langapp.red.incr')
  def test_try_it_the_proper_way(self, redis_incr):
    self.app.post('/in/', data='doesnt matter')
    redis_incr.assert_called_once_with('messageid')


if __name__ == '__main__':
  unittest.main()
