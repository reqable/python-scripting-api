import unittest
import json
import main

class MainTest(unittest.TestCase):
  def testRequest(self):
    main.onRequest('request.json')
    with open('request.json.cb', 'r', encoding='UTF-8') as content:
      request = json.load(content)['request']
    self.assertEqual(request['headers'][-1], 'signature: 3e8c6c3b1cdca44384d0beaa487dbd21')

if __name__ == '__main__':
  unittest.main()