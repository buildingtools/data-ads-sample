import json
from django.http import HttpResponse


class ApiError(Exception):
    """
    Handler for Errors
    """
    def __init__(self, message):
        self.message = message


    def __str__(self):
        return repr("%s" % (self.message))
