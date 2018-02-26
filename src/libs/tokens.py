# serializer for JWT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from libs import util
import time

conf = util.conf_path()
"""
    token is generated as the JWT protocol.
    JSON Web Tokens(JWT) are an open, industry standard RFC 7519 method
"""
def genTokenSeq(self, expires):
        s = Serializer(
            secret_key=conf.config['SECRET_KEY'],
            salt=conf.config['AUTH_SALT'],
            expires_in=expires)
        timestamp = time.time()
        return s.dumps(
            {'user_id': self.user_id,
             'user_role': self.role_id,
             'iat': timestamp})
        # The token contains userid, user role and the token generation time.
        # u can add sth more inside, if needed.
        # 'iat' means 'issued at'. claimed in JWT.