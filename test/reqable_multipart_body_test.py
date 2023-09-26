import unittest

from reqable import CaptureHttpMultipartBody as multipart

class HttpMultipartBodyTest(unittest.TestCase):
  def testHttpMultipartBodyConstructor(self):
    body = multipart({
      'headers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 1,
        'payload': 'Hello World'
      }
    })
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, 'Hello World')
    self.assertEqual(body.headers.entries, [
      'foo: bar',
      'abc: 123',
      'hello: world'
    ])

    body = multipart.text('Hi World', 'python', 'image.png', [
      'abc: 123',
      'foo: bar'
    ])
    self.assertEqual(body.type, 1)
    self.assertEqual(body.payload, 'Hi World')
    self.assertEqual(body.headers.entries, [
      'abc: 123',
      'foo: bar',
      'content-length: 8',
      'content-disposition: form-data; name="python"; filename="image.png"'
    ])

    body = multipart.text('Hi World')
    self.assertEqual(body.headers.entries, [
      'content-length: 8',
    ])

    body = multipart.text('Hi World', name = 'python')
    self.assertEqual(body.headers.entries, [
      'content-length: 8',
      'content-disposition: form-data; name="python"'
    ])

    body = multipart.text('Hi World', filename = 'image.png')
    self.assertEqual(body.headers.entries, [
      'content-length: 8',
      'content-disposition: form-data; filename="image.png"'
    ])

    body = multipart.file('data/body_binary.bin', 'python', 'image.png', [
      'abc: 123',
      'foo: bar'
    ])
    self.assertEqual(body.type, 2)
    self.assertEqual(body.payload, b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
    self.assertEqual(body.headers.entries, [
      'abc: 123',
      'foo: bar',
      'content-length: 8',
      'content-disposition: form-data; name="python"; filename="image.png"'
    ])


  def testHttpMultipartBodySerialize(self):
    data = {
      'headers': [
        'foo: bar',
        'abc: 123',
        'hello: world'
      ],
      'body': {
        'type': 1,
        'payload': 'Hello World'
      }
    }
    body = multipart(data)
    self.assertEqual(body.serialize(), data)


if __name__ == '__main__':
  unittest.main()