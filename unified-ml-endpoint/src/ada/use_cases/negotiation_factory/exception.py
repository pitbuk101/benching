"""Exception class for Negotiation Factory use case"""


class NegotiationFactoryUserException(Exception):
    """
    Instantiated for Negotiation Factory Error which Needs to informed to user
    """


class NegotiationFactoryException(Exception):
    """
    Instantiated for Negotiation Factory exception
    """


class NegotiationFactoryQueryException(Exception):
    """
    Instantiated for Negotiation Factory exception when data not found based on user request
    """
