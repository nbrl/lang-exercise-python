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
    langapp.red.incr.return_value = 1
    self.app.post('/in/', data='some data')
    redis_hset.assert_called_once_with('messages', 1, 'some data')

  @mock.patch('langapp.red.hset')
  def test_new_message_added_to_hash_url_enc_type(self, redis_hset):
    langapp.red.incr.return_value = 1
    self.app.post('/in/', data='some%20data', headers={'content-type':'application/x-www-form-urlencoded'})
    redis_hset.assert_called_once_with('messages', 1, 'some data')


class LangAppGetMessage(unittest.TestCase):
  def setUp(self):
    self.app = langapp.app.test_client()
    self.redisPatcher = mock.patch('langapp.red')
    self.mockRedis = self.redisPatcher.start()

  def tearDown(self):
    self.redisPatcher.stop()
    pass

  def test_check_test_env_is_sane(self):
    assert langapp.red is self.mockRedis

  @mock.patch('langapp.red.hexists')
  def test_existance_of_correct_message_checked(self, redis_hexists):
    mid = 12
    self.app.get('/messages/' + str(mid) + '/')
    redis_hexists.assert_called_once_with('messages', mid)

  @mock.patch('langapp.red.hexists')
  def test_get_incorrect_message(self, redis_hexists):
    redis_hexists.return_value = False
    rv = self.app.get('/messages/123/')
    self.assertEqual(rv.status_code, 404)
    self.assertEqual(rv.data, 'no such message')

  @mock.patch('langapp.red.hexists')
  @mock.patch('langapp.red.hget')
  def test_get_existing_message(self, redis_hexists, redis_hget):
    # This test doesn't return properly, i.e. rv.data is a 500...
    mid = 12
    redis_hexists.return_value = True
    redis_hget.return_value('hello world!')
    rv = self.app.get('/messages/' + str(mid) + '/')
    redis_hexists.assert_called_once_with('messages', mid)
    redis_hget.assert_called_once_with('messages', mid)

if __name__ == '__main__':
  unittest.main(verbosity = 2)
