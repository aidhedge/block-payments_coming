from logger import Logger
LOG = Logger()
class baseExpcetion(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['message'] = self.message
        LOG.console(rv)
        return rv

class payLoadIsMissing(baseExpcetion):
    pass

class malformedJson(baseExpcetion):
    pass

class payloadNotMatchingSchema(baseExpcetion):
    pass

class NotAbleToConnectToSourceApi(baseExpcetion):
    pass 

class NoAPIKeyPresent(baseExpcetion):
    pass



