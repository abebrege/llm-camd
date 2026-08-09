from hashlib import pbkdf2_hmac

pbkdf2_hmac('sha256', b'SomePasswordThatExceeds32CharactersInLength',
            b'NotLong', 100000)
