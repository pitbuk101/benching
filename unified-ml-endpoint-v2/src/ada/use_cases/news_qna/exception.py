"""Exception classes for news QnA Use case"""


class NewsQnAException(Exception):
    """Custom exception class for handling errors specific to the News QnA application."""


class SupplierNotFoundException(Exception):
    """Raised when supplier name not found in user query"""

    def __init__(self, message: str = None):
        if message is None:
            message = (
                "Supplier name not found in query.\n"
                "Ada couldn't be able to answer this question for now"
            )
        self.message = message
        super().__init__(self.message)


class NoNewsFoundException(Exception):
    """Raised when no news found for user query"""

    def __init__(self, message: str = None):
        if message is None:
            message = "We could not find any news for given prompt"
        self.message = message
        super().__init__(self.message)


class CategoryNotMatchedException(Exception):
    """Raised when user selected category and category in user query does not match"""

    def __init__(self, selected_category: str, question_category: str):
        self.message = (
            f"Your selected category {selected_category} is not matching "
            f"with the category in question {question_category}"
        )
        super().__init__(self.message)
