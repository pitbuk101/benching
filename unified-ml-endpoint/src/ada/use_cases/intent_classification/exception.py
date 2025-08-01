"""Exception classes for intent classifier model"""


class OutOfScopeIntentException(Exception):
    """Raised when intent is not from expected intent list"""


class IntentModelUserException(Exception):
    """Raised when required key is not present in payload"""
