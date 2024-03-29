from functools import wraps

from arbeitszeit_flask.dependency_injection import with_injection
from arbeitszeit_web.api.authentication import Authenticator


@with_injection()
def authentication_check(func, authenticator: Authenticator):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        authenticator.authenticate_request()
        return func(*args, **kwargs)

    return decorated_function
