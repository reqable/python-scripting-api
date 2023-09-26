import unittest

from reqable import CaptureHttpRequest

class HttpRequestTest(unittest.TestCase):
  def testHttpRequestConstructor(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
      'headers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 0,
        'payload': None
      },
    })
    self.assertEqual(request.method, 'GET')
    self.assertEqual(request.path, '/')
    self.assertEqual(request.protocol, 'HTTP/1.1')
    self.assertEqual(request.queries.entries, [])
    self.assertEqual(request.headers.entries, [
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])
    self.assertEqual(request.body.type, 0)
    self.assertEqual(request.body.payload, None)
    self.assertEqual(request.trailers.entries, [])

    request = CaptureHttpRequest({
      'method': 'POST',
      'path': '/good?python=good&name=megatron',
      'protocol': 'h2',
      'trailers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ]
    })
    self.assertEqual(request.method, 'POST')
    self.assertEqual(request.path, '/good')
    self.assertEqual(request.protocol, 'h2')
    self.assertEqual(request.queries.entries, [
      ('python', 'good'),
      ('name', 'megatron'),
    ])
    self.assertEqual(request.headers.entries, [])
    self.assertEqual(request.trailers.entries, [
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])


  def testHttpRequestMethodUpdate(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
    })

    request.method = 'DELETE'
    self.assertEqual(request.method, 'DELETE')


  def testHttpRequestPathUpdate(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
    })
    request.path = '/abc'
    self.assertEqual(request.path, '/abc')


  def testHttpRequestQueriesUpdate(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
    })
    request.queries['foo'] = 'bar'
    self.assertEqual(request.queries.entries, [
      ('foo', 'bar'),
    ])
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/good?python=good&name=megatron',
      'protocol': 'HTTP/1.1',
    })
    request.queries['foo'] = 'bar'
    self.assertEqual(request.queries.entries, [
      ('python', 'good'),
      ('name', 'megatron'),
      ('foo', 'bar'),
    ])

    request.queries.clear()
    self.assertEqual(request.queries.entries, [])

    request.queries = 'python=good&name=megatron'
    self.assertEqual(request.queries.entries, [
      ('python', 'good'),
      ('name', 'megatron'),
    ])

    request.queries = {
      'foo': 'bar'
    }
    self.assertEqual(request.queries.entries, [
      ('foo', 'bar'),
    ])
    request.queries = [
      ('foo', 'bar')
    ]
    self.assertEqual(request.queries.entries, [
      ('foo', 'bar'),
    ])


  def testHttpRequestHeadersUpdate(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
    })
    request.headers['foo'] = 'bar'
    self.assertEqual(request.headers.entries, [
      'foo: bar'
    ])
    request.headers['name'] = 'megatron'
    self.assertEqual(request.headers.entries, [
      'foo: bar',
      'name: megatron'
    ])
    request.headers = [
      'foo: bar',
      'abc: 123'
    ]
    self.assertEqual(request.headers.entries, [
      'foo: bar',
      'abc: 123'
    ])
    request.headers = {
      'foo': 'bar',
      'abc': '123',
    }
    self.assertEqual(request.headers.entries, [
      'foo: bar',
      'abc: 123'
    ])
    request.headers = [
      ('foo', 'bar'),
      ('abc', '123'),
    ]
    self.assertEqual(request.headers.entries, [
      'foo: bar',
      'abc: 123'
    ])

  def testHttpRequestTrailersUpdate(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
    })
    request.trailers['foo'] = 'bar'
    self.assertEqual(request.trailers.entries, [
      'foo: bar'
    ])
    request.trailers['name'] = 'megatron'
    self.assertEqual(request.trailers.entries, [
      'foo: bar',
      'name: megatron'
    ])
    request.trailers = [
      'foo: bar',
      'abc: 123'
    ]
    self.assertEqual(request.trailers.entries, [
      'foo: bar',
      'abc: 123'
    ])

  def testHttpRequestBodyUpdate(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
    })
    request.body = 'Hello World'
    self.assertTrue(request.body.isText)
    self.assertEqual(request.body.payload, 'Hello World')

    request.body = {
      'foo': 'bar',
      'abc': 123
    }
    self.assertTrue(request.body.isText)
    self.assertEqual(request.body.payload, '{"foo": "bar", "abc": 123}')

    request.body = b'\x01\x02\x03\x04'
    self.assertTrue(request.body.isBinary)
    self.assertEqual(request.body.payload, b'\x01\x02\x03\x04')


  def testHttpRequestContentType(self):
    request = CaptureHttpRequest({
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
      'headers': [
        'content-type: text/palin; charset=utf-8',
      ],
    })
    self.assertEqual(request.contentType, 'text/palin; charset=utf-8')
    self.assertEqual(request.mime, 'text/palin')

  def testHttpRequestSerialize(self):
    data = {
      'method': 'GET',
      'path': '/',
      'protocol': 'HTTP/1.1',
      'headers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 1,
        'payload': 'Hello World'
      },
      'trailers': []
    }
    request = CaptureHttpRequest(data)
    self.assertEqual(request.serialize(), data)

    request.method = 'POST'
    request.path = '/abc'
    request.queries['foo'] = 'bar'
    request.headers.remove('foo')
    request.body = 'Reqable'
    request.trailers['abc'] = '123'
    self.assertEqual(request.serialize(), {
      'method': 'POST',
      'path': '/abc?foo=bar',
      'protocol': 'HTTP/1.1',
      'headers': [
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 1,
        'payload': 'Reqable'
      },
      'trailers': [
        'abc: 123',
      ]
    })

if __name__ == '__main__':
  unittest.main()