from typing import Optional

from pydantic import BaseModel


# default request schema
class QueryRequest(BaseModel):
    query: str
    use_driver: bool = True


# default response schema
class QueryResponse(BaseModel):
    original_query: str
    result: Optional[dict] = None
    count: int = 0
    status_code: int


class ErrorResponse(BaseModel):
    error: str
    status_code: int


class CreateAskingTaskModel(BaseModel):
    operationName: str = "CreateAskingTask"
    variables: Optional[dict] = None
    query: str = """mutation CreateAskingTask($data: AskingTaskInput!)
        {\n  createAskingTask(data: $data) {\n    id\n    __typename\n  }\n}"""

    def __init__(self, question):
        super().__init__()
        self.variables = {
            "data": {
                "question": question,
            },
        }


class AskingTaskModel(BaseModel):
    operationName: str = "AskingTask"
    variables: Optional[dict] = None
    query: str = """
                    query AskingTask($taskId: String!) {
                    askingTask(taskId: $taskId) {
                        status
                        type
                        candidates {
                        sql
                        type
                        view {
                            id
                            name
                            statement
                            displayName
                            __typename
                        }
                        __typename
                        }
                        error {
                        ...CommonError
                        __typename
                        }
                        __typename
                    }
                    }

                    fragment CommonError on Error {
                    code
                    shortMessage
                    message
                    stacktrace
                    __typename
                    }
                    """

    def __init__(self, taskId):
        super().__init__()
        self.variables = {
            "taskId": taskId,
        }


class CreateThreadModel(BaseModel):
    operationName: str = "CreateThread"
    variables: Optional[dict] = None
    query: str = """
                    mutation CreateThread($data: CreateThreadInput!) {
                    createThread(data: $data) {
                        id
                        sql
                        __typename
                    }
                    }
                """

    def __init__(self, sql, question):
        super().__init__()
        self.variables = {
            "data": {
                "sql": sql,
                "question": question,
            },
        }


class ThreadModel(BaseModel):
    operationName: str = "Thread"
    variables: Optional[dict] = None
    query: str = """
                    query Thread($threadId: Int!) {
                    thread(threadId: $threadId) {
                        id
                        sql
                        responses {
                        ...CommonResponse
                        error {
                            ...CommonError
                            __typename
                        }
                        __typename
                        }
                        __typename
                    }
                    }

                    fragment CommonResponse on ThreadResponse {
                    id
                    question
                    status
                    detail {
                        sql
                        description
                        steps {
                        summary
                        sql
                        cteName
                        __typename
                        }
                        view {
                        id
                        name
                        statement
                        displayName
                        __typename
                        }
                        __typename
                    }
                    __typename
                    }

                    fragment CommonError on Error {
                    code
                    shortMessage
                    message
                    stacktrace
                    __typename
                    }
                    """

    def __init__(self, threadId):
        super().__init__()
        self.variables = {
            "threadId": threadId,
        }


class ThreadResponseModel(BaseModel):
    operationName: Optional[str] = "ThreadResponse"
    variables: Optional[dict] = None
    query: Optional[
        str
    ] = """query ThreadResponse($responseId: Int!) {
                                threadResponse(responseId: $responseId) {
                                ...CommonResponse
                                error {
                                ...CommonError
                                __typename
                                }
                                __typename
                            }
                            }
                            fragment CommonResponse on ThreadResponse {
                            id
                            question
                            status
                            detail {
                                sql
                                description
                                steps {
                                summary
                                sql
                                cteName
                                __typename
                                }
                                view {
                                id
                                name
                                statement
                                displayName
                                __typename
                                }
                                __typename
                            }
                            __typename
                            }

                            fragment CommonError on Error {
                            code
                            shortMessage
                            message
                            stacktrace
                            __typename
                            }"""

    def __init__(self, responseId):
        super().__init__()
        self.variables = {
            "responseId": responseId,
        }


class PreviewDataModel(BaseModel):
    operationName: Optional[str] = "PreviewData"
    variables: Optional[dict] = None
    template: str = "mutation PreviewData($where: PreviewDataInput!){previewData(where: $where)}"
    query: Optional[str] = template

    def __init__(self, response_id, stepIndex):
        super().__init__()
        self.variables = {
            "where": {
                "responseId": response_id,
                "stepIndex": stepIndex,
            },
        }
