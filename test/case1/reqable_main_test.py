import unittest
import json
import main

class MainTest(unittest.TestCase):
  def testRequest(self):
    main.onRequest('request.json')
    with open('request.json', 'r', encoding='UTF-8') as content:
      dict1 = json.load(content)
    with open('request.json.cb', 'r', encoding='UTF-8') as content:
      dict2 = json.load(content)
    self.assertEqual(dict1['request'], dict2['request'])
    self.assertEqual(dict2['shared'], None)

  def testResponse(self):
    main.onResponse('response.json')
    with open('response.json', 'r', encoding='UTF-8') as content:
      dict1 = json.load(content)
    with open('response.json.cb', 'r', encoding='UTF-8') as content:
      dict2 = json.load(content) 
    self.assertEqual(dict1['response'], dict2['response'])     


if __name__ == '__main__':
  unittest.main()