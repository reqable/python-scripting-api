import unittest
import json
import main

class MainTest(unittest.TestCase):
  def testRequest(self):
    main.onRequest('request.json')
    with open('request.json.cb', 'r', encoding='UTF-8') as content:
      shared = json.load(content)['shared']
      self.assertEqual(shared, 1)

  def testResponse(self):
    main.onResponse('response.json')
    with open('response.json.cb', 'r', encoding='UTF-8') as content:
      shared = json.load(content)['shared']
      self.assertEqual(shared, 2)


if __name__ == '__main__':
  unittest.main()