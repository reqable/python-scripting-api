import unittest

from reqable import CaptureContext

class ContextTest(unittest.TestCase):
  def testContextConstructor(self):
    context = CaptureContext({
      'url': 'https://reqable.com',
      'scheme': 'https',
      'host': 'reqable.com',
      'port': 443,
      'cid': 32,
      'ctime': 1686556178335,
      'sid': 7,
      'stime': 1686556256263,
      'env': {
        'foo': 'bar',
        'abc': '123',
        '$randomEmail': 'random@reqable.com'
      }
    })
    self.assertEqual(context.url, 'https://reqable.com')
    self.assertEqual(context.scheme, 'https')
    self.assertEqual(context.host, 'reqable.com')
    self.assertEqual(context.port, 443)
    self.assertEqual(context.cid, 32)
    self.assertEqual(context.ctime, 1686556178335)
    self.assertEqual(context.sid, 7)
    self.assertEqual(context.stime, 1686556256263)
    self.assertEqual(context.uid, '1686556178335-32-7')
    self.assertEqual(context.env['foo'], 'bar')
    self.assertEqual(context.env['abc'], '123')
    self.assertEqual(context.env['$randomEmail'], 'random@reqable.com')

if __name__ == '__main__':
  unittest.main()