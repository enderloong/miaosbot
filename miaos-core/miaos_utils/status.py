
class MiaosErrorBase(Exception):
    error_code = 99999
    error_msg = "Miaos error base"
    raw_error = None

    def __init__(self, e=None, tb=None, msg=None):
        if isinstance(e, Exception):
            self.error_msg += '; Error: {}'.format(str(e))
            self.raw_error = e
        if tb is not None:
            self.error_msg += '; Traceback: {}'.format(tb)
        if msg is not None:
            self.error_msg += ';' + msg

class MiaosParameterError(MiaosErrorBase):
    error_code = 40000
    error_msg = 'Miaos server got wrong parameters'
    
class MiaosDropTimeoutRequestError(MiaosErrorBase):
    error_code = 40800
    error_msg = 'This request is outdated. Miaos will ignore it'