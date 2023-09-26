import unittest

from reqable import CaptureHttpHeaders

class HttpHeadersTest(unittest.TestCase):
  def testHttpHeadersConstructor(self):
    headers = CaptureHttpHeaders()
    self.assertEqual(len(headers), 0)
    self.assertEqual(headers.entries, [])

    headers = CaptureHttpHeaders(None)
    self.assertEqual(len(headers), 0)
    self.assertEqual(headers.entries, [])

    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(len(headers), 3)
    self.assertEqual(headers['foo'], 'bar')
    self.assertEqual(headers['abc'], '123')
    self.assertEqual(headers['hello'], 'world')
    self.assertEqual(headers['python'], None)

    headers = CaptureHttpHeaders.of([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(len(headers), 3)
    self.assertEqual(headers['foo'], 'bar')
    self.assertEqual(headers['abc'], '123')
    self.assertEqual(headers['hello'], 'world')

    headers = CaptureHttpHeaders.of({
      'foo': 'bar',
      'abc': '123',
      'hello': 'world'
    })
    self.assertEqual(len(headers), 3)
    self.assertEqual(headers['foo'], 'bar')
    self.assertEqual(headers['abc'], '123')
    self.assertEqual(headers['hello'], 'world')

    headers = CaptureHttpHeaders.of([
      ('foo', 'bar'),
      ('abc', '123'),
      ('hello', 'world')
    ])
    self.assertEqual(len(headers), 3)
    self.assertEqual(headers['foo'], 'bar')
    self.assertEqual(headers['abc'], '123')
    self.assertEqual(headers['hello'], 'world')


  def testHttpHeadersUpdate(self):
    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    headers.add('python', 'good')
    self.assertEqual(headers['python'], 'good')
    self.assertEqual(len(headers), 4)

    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    headers['python'] = 'good'
    self.assertEqual(headers['python'], 'good')
    self.assertEqual(len(headers), 4)

    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    headers['foo'] = 'reqable'
    self.assertEqual(headers['foo'], 'reqable')
    self.assertEqual(len(headers), 3)

    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    headers.remove('foo')
    self.assertEqual(headers['foo'], None)
    self.assertEqual(len(headers), 2)

    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    headers.clear()
    self.assertEqual(len(headers), 0)

  def testHttpQueriesIndex(self):
    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world',
    ])
    self.assertEqual(headers.index('foo'), 0)
    self.assertEqual(headers.index('abc'), 1)
    self.assertEqual(headers.index('hello'), 2)

    self.assertEqual(headers[0], 'foo: bar')
    self.assertEqual(headers[1], 'abc: 123')
    self.assertEqual(headers[2], 'hello: world')


  def testHttpHeadersDunplicateName(self):
    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world',
      'foo: good',
    ])
    self.assertEqual(headers.index('foo'), 0)
    self.assertEqual(headers.indexes('foo'), [0, 3])
    self.assertEqual(headers['foo'], 'bar')


  def testHttpHeadersPrint(self):
    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(str(headers), "['foo: bar', 'abc: 123', 'hello: world']")


  def testHttpHeadersIterator(self):
    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    it = iter(headers)
    self.assertEqual(next(it), 'foo: bar')
    self.assertEqual(next(it), 'abc: 123')
    self.assertEqual(next(it), 'hello: world')


  def testHttpHeadersCasesensive(self):
    headers = CaptureHttpHeaders([
      'Foo: bar',
      'Abc: 123',
      'Hello: world'
    ])
    self.assertEqual(headers['foo'], 'bar')
    self.assertEqual(headers['abc'], '123')
    self.assertEqual(headers['hello'], 'world')

    headers = CaptureHttpHeaders([
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(headers['Foo'], 'bar')
    self.assertEqual(headers['Abc'], '123')
    self.assertEqual(headers['Hello'], 'world')
    headers = CaptureHttpHeaders([
      'FOO: BAR',
      'ABC: 123',
      'HELLO: WORLD'
    ])

    self.assertEqual(headers['foo'], 'BAR')
    self.assertEqual(headers['abc'], '123')
    self.assertEqual(headers['hello'], 'WORLD')

if __name__ == '__main__':
  unittest.main()