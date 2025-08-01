"""Custom Parsers for dynamic ideas and QnA use-case"""

from pydantic import BaseModel, field_validator

from ada.utils.config.config_loader import read_config

dynamic_ideas_conf = read_config("use-cases.yml")["dynamic_ideas"]


class RequestPayload(BaseModel):
    """Model for dynamic ideas request parameters and validation of parameters"""

    user_query: str
    request_type: str
    page_id: str
    category: str
    tenant_id: str

    @field_validator("request_type")
    @classmethod
    def validate_request_type(cls, value):
        """To validate 'request_type' parameter in request"""
        if value not in dynamic_ideas_conf["supported_request_types"]:
            raise ValueError(
                f"""Unsupported 'request_type': {value}.
                Must be one of {dynamic_ideas_conf['supported_request_types']}.""",
            )
        return value

    @field_validator("page_id")
    @classmethod
    def validate_page_id(cls, value):
        """To validate 'page_id' parameter in request"""
        if value not in dynamic_ideas_conf["supported_page_ids"]:
            raise ValueError(
                f"""Unsupported 'page_id': {value}.
                Must be one of {dynamic_ideas_conf['supported_page_ids']}.""",
            )
        return value

    @field_validator("user_query")
    @classmethod
    def validate_user_query(cls, value):
        """To validate 'user_query' parameter in request"""
        if not value or not value.strip():
            raise ValueError("user_query must not be empty or None.")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        """To validate 'category' parameter in request"""
        if not value or not value.strip():
            raise ValueError("category must not be empty or None.")
        return value

    @field_validator("tenant_id")
    @classmethod
    def validate_tenant_id(cls, value):
        """To validate 'tenant_id' parameter in request"""
        if not value or not value.strip():
            raise ValueError("tenant_id must not be empty or None.")
        return value
