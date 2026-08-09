from hashlib import pbkdf2_hmac

hash = pbkdf2_hmac('sha256', b'SomePasswordThatExceeds32CharactersInLength',
                   b'D8VxSmTZt2E2YV454mkqAY5e', 100000)
