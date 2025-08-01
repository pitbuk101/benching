import os


def pop_excess_environment_variables():
    """
    Pop excess environment variables.
    """
    if os.getenv("AZURE_OPENAI_API_BASE"):
        os.environ.pop("AZURE_OPENAI_API_BASE")