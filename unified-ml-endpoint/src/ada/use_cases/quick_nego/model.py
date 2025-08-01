from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

# ASSISTANT_ID = "asst_vgrJzHYxHGYwGzVbRenYSdRg"
ASSISTANT_ID = "asst_AdK66npCY5KcJu4t3XqRuD2d"
DEFAULT_TENANT_ID = "920a2f73-c7db-405f-98ea-f768c6da864f"
DEFAULT_TENANT_ID_MESSAGE = "Tenant ID cannot be empty"
WELCOME_MESSAGE = """
Welcome! I'm your McKinsey procurement consultant. I'll guide you through developing 
a comprehensive negotiation strategy using our proven framework.

We'll systematically work through:
• Supplier intelligence and market dynamics
• Key negotiation levers and power analysis  
• BATNA (Best Alternative) development
• ZOPA (Zone of Possible Agreement) mapping
• Strategic negotiation approach
• Professional negotiation email drafting

Let's begin. What's the name of the supplier you're preparing to negotiate with?
"""
class CurrencySymbol(str, Enum):
    EUR = "€"
    USD = "$"
    BRL = "R$"
    TRY = "₺"
    ZAR = "R"
    CNY = "¥"
    HUF = "Ft"
    INR = "₹"
    GBP = "£"
    CZK = "Kč"
    CHF = "Fr"
    JPY = "¥"
    AUD = "A$"
    CAD = "C$"
    NOK = "kr"
    SEK = "kr"
    DKK = "kr"
    PLN = "zł"
    MXN = "$"
    SGD = "S$"
    HKD = "HK$"
    KRW = "₩"
    IDR = "Rp"
    THB = "฿"
    MYR = "RM"
    RUB = "₽"
    ILS = "₪"
    TWD = "NT$"
    VND = "₫"

class BaseNegoModel(BaseModel):
    model_config = {"extra": "forbid"}
class ResponseStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
class QuickNegoRequest(BaseNegoModel):
    thread_id: str
    message: str
    model_config = {"extra": "forbid"}
    @field_validator('thread_id')
    @classmethod
    def validate_thread_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Thread ID cannot be empty')
        return v.strip()
    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
# Simplified models for faster response times
class QuickNegoResponse(BaseNegoModel):
    reply: str
    status: ResponseStatus
    
class SupplierResponse(BaseNegoModel):
    supplier_data: List[Dict[str, Any]] = []

class SupplierRequest(BaseNegoModel):
    tenant_id: str
    category: str
    @field_validator('tenant_id')
    @classmethod
    def validate_tenant_id(cls, v):
        if not v or not v.strip():
            raise ValueError(DEFAULT_TENANT_ID_MESSAGE)
        return v.strip()
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if not v or not v.strip():
            raise ValueError('Category cannot be empty')
        return v.strip()


class SKURequest(BaseNegoModel):
    supplier_name: str
    tenant_id: str
    category:str
    
    @field_validator('supplier_name')
    @classmethod
    def validate_supplier_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Supplier name cannot be empty')
        return v.strip()
    
    @field_validator('tenant_id')
    @classmethod
    def validate_tenant_id(cls, v):
        if not v or not v.strip():
            raise ValueError(DEFAULT_TENANT_ID_MESSAGE)
        return v.strip()
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if not v or not v.strip():
            raise ValueError('Category cannot be empty')
        return v.strip()
class SKUResponse(BaseNegoModel):
    skus: List[Dict[str, Any]] = []


class ConversationStartResponse(BaseNegoModel):
    thread_id: str
    welcome_message: str
    status: str = "success"

class AnalysisStartResponse(BaseNegoModel):
    status: ResponseStatus  # "completed", "success", "done"
    message: str  # "Analysis completed successfully"
    thread_id: str
class AnalysisStartRequest(BaseNegoModel):
    tenant_id: str
    supplier_name: str
    category_name: str
    sku: List[str] | str
    thread_id:str

    @field_validator('tenant_id')
    @classmethod
    def validate_tenant_id(cls, v):
        if not v or not v.strip():
            raise ValueError(DEFAULT_TENANT_ID_MESSAGE)
        return v.strip()

    @field_validator('thread_id')
    @classmethod
    def validate_tenant_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Thread ID cannot be empty')
        return v.strip()

    @field_validator('supplier_name')
    @classmethod
    def validate_supplier_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Supplier name cannot be empty')
        return v.strip()

    @field_validator('category_name')
    @classmethod
    def validate_category_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Category name cannot be empty')
        return v.strip()

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v):
        if isinstance(v, list):
            if not v:  # Empty list
                raise ValueError('SKU list cannot be empty')
            # Validate each SKU in the list
            validated_skus = []
            for sku in v:
                if not sku or not str(sku).strip():
                    raise ValueError('SKU cannot be empty')
                validated_skus.append(str(sku).strip())
            return validated_skus
        else:  # Single string
            if not v or not str(v).strip():
                raise ValueError('SKU cannot be empty')
            return str(v).strip()
