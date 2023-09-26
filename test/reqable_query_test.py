import unittest

from reqable import CaptureHttpQueries

class HttpQueriesTest(unittest.TestCase):
  def testHttpQueriesConstructor(self):
    queries = CaptureHttpQueries()
    self.assertEqual(len(queries), 0)
    self.assertEqual(queries.entries, [])

    queries = CaptureHttpQueries([])
    self.assertEqual(len(queries), 0)
    self.assertEqual(queries.entries, [])

    queries = CaptureHttpQueries(None)
    self.assertEqual(len(queries), 0)
    self.assertEqual(queries.entries, [])

    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    self.assertEqual(len(queries), 3)
    self.assertEqual(queries['foo'], 'bar')
    self.assertEqual(queries['abc'], '123')
    self.assertEqual(queries['hello'], 'world')
    self.assertEqual(queries['python'], None)

    queries = CaptureHttpQueries.of('foo=bar&abc=123&hello=world')
    self.assertEqual(len(queries), 3)
    self.assertEqual(queries['foo'], 'bar')
    self.assertEqual(queries['abc'], '123')
    self.assertEqual(queries['hello'], 'world')

    queries = CaptureHttpQueries.parse('url=https%3A%2F%2Freqable.com')
    self.assertEqual(len(queries), 1)
    self.assertEqual(queries['url'], 'https://reqable.com')

    queries = CaptureHttpQueries.of('url=https%3A%2F%2Freqable.com')
    self.assertEqual(len(queries), 1)
    self.assertEqual(queries['url'], 'https://reqable.com')

    queries = CaptureHttpQueries.parse('foo')
    self.assertEqual(len(queries), 1)
    self.assertEqual(queries['foo'], '')

    queries = CaptureHttpQueries.parse('')
    self.assertEqual(len(queries), 0)

    queries = CaptureHttpQueries.of({
      'foo': 'bar',
      'abc': '123'
    })
    self.assertEqual(len(queries), 2)
    self.assertEqual(queries['foo'], 'bar')
    self.assertEqual(queries['abc'], '123')

    self.assertRaises(Exception, CaptureHttpQueries.of, {
      'foo': 'bar',
      'abc': 123
    })

    queries = CaptureHttpQueries.of([
      ('foo', 'bar'),
      ('abc', '123')
    ])
    self.assertEqual(len(queries), 2)
    self.assertEqual(queries['foo'], 'bar')
    self.assertEqual(queries['abc'], '123')

    self.assertRaises(Exception, CaptureHttpQueries.of, {
      ('foo', 'bar'),
      ('abc', 123)
    })


  def testHttpQueriesUpdate(self):
    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    queries.add('python', 'good')
    self.assertEqual(queries['python'], 'good')
    self.assertEqual(len(queries), 4)

    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    queries['python'] = 'good'
    self.assertEqual(queries['python'], 'good')
    self.assertEqual(len(queries), 4)

    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    queries['foo'] = 'reqable'
    self.assertEqual(queries['foo'], 'reqable')
    self.assertEqual(len(queries), 3)

    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    queries.remove('foo')
    self.assertEqual(queries['foo'], None)
    self.assertEqual(len(queries), 2)

    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    queries.clear()
    self.assertEqual(len(queries), 0)


  def testHttpQueriesIterator(self):
    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    it = iter(queries)
    self.assertEqual(next(it), ('foo', 'bar'))
    self.assertEqual(next(it), ('abc', '123'))
    self.assertEqual(next(it), ('hello', 'world'))


  def testHttpQueriesIndex(self):
    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    self.assertEqual(queries.index('foo'), 0)
    self.assertEqual(queries.index('abc'), 1)
    self.assertEqual(queries.index('hello'), 2)

    self.assertEqual(queries[0], ('foo', 'bar'))
    self.assertEqual(queries[1], ('abc', '123'))
    self.assertEqual(queries[2], ('hello', 'world'))

  def testHttpQueriesDunplicateName(self):
    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world&foo=good')
    self.assertEqual(queries.index('foo'), 0)
    self.assertEqual(queries.indexes('foo'), [0, 3])
    self.assertEqual(queries['foo'], 'bar')


  def testHttpQueriesPrint(self):
    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    self.assertEqual(str(queries), "[('foo', 'bar'), ('abc', '123'), ('hello', 'world')]")


  def testHttpQueriesConcat(self):
    queries = CaptureHttpQueries.parse('foo=bar&abc=123&hello=world')
    self.assertEqual(queries.concat(), 'foo=bar&abc=123&hello=world')
    self.assertEqual(queries.concat(encode=True), 'foo=bar&abc=123&hello=world')

    queries = CaptureHttpQueries.parse('foo=bar&abc=123&url=https%3A%2F%2Freqable.com')
    self.assertEqual(queries.concat(), 'foo=bar&abc=123&url=https%3A%2F%2Freqable.com')
    self.assertEqual(queries.concat(encode=True), 'foo=bar&abc=123&url=https%3A%2F%2Freqable.com')
    self.assertEqual(queries.concat(encode=False), 'foo=bar&abc=123&url=https://reqable.com')

if __name__ == '__main__':
  unittest.main()