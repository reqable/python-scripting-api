import unittest
import json
import main

class MainTest(unittest.TestCase):
  def testRequest(self):
    main.onRequest('request.json')
    with open('request.json.cb', 'r', encoding='UTF-8') as content:
      request = json.load(content)['request']
    self.assertEqual(request['method'], 'HEAD')
    self.assertEqual(request['path'], '/abc?foo=bar')
    self.assertEqual(request['headers'][-1], 'foo: bar')
    self.assertEqual(request['trailers'][-1], 'foo: bar')
    self.assertEqual(request['body']['type'], 1)
    self.assertEqual(request['body']['payload'], 'foobar')

  def testResponse(self):
    main.onResponse('response.json')
    with open('response.json.cb', 'r', encoding='UTF-8') as content:
      response = json.load(content)['response']
    self.assertEqual(response['code'], 404)
    self.assertEqual(response['headers'][-1], 'foo: bar')
    self.assertEqual(response['trailers'][-1], 'foo: bar')
    self.assertEqual(response['body']['type'], 1)
    self.assertEqual(response['body']['payload'], 'foobar')


if __name__ == '__main__':
  unittest.main()