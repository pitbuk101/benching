from typing import Any, List, Optional
from pydantic import BaseModel, Field


class PaymentTerms(BaseModel):
    domestic: Optional[int] = Field(None, alias="domestic")
    export: Optional[int] = Field(None, alias="export")


class Prices(BaseModel):
    unit: Optional[Any] = Field(None, alias="unit")
    lump_sum: Optional[Any] = Field(None, alias="lump sum")
    item_level: Optional[Any] = Field(None, alias="item-level")
    aggregate_level: Optional[Any] = Field(None, alias="aggregate-level")
    discount_conditions: Optional[Any] = Field(None, alias="discount conditions")


class SKUInfo(BaseModel):
    product_id: Optional[str] = Field(None, alias="product ID")
    description: Optional[str] = Field(None, alias="description")
    quantity_per_sku: Optional[Any] = Field(None, alias="quantity per SKU")
    unit_price: Optional[Any] = Field(None, alias="unit_price")


class PaymentInvoicingTerms(BaseModel):
    invoice_requirements: Optional[List[str]] = Field(default_factory=list, alias="Invoice requirements")
    invoice_submission: Optional[str] = Field(None, alias="Invoice submission")


class InsuranceCoverage(BaseModel):
    type: Optional[str] = Field(None, alias="type")
    sum_insured: Optional[str] = Field(None, alias="sum_insured")
    due_date: Optional[str] = Field(None, alias="due_date")


class Insurance(BaseModel):
    coverage: Optional[List[InsuranceCoverage]] = Field(default_factory=list, alias="coverage")
    types: Optional[List[str]] = Field(default_factory=list, alias="types")


class VendorInfo(BaseModel):
    name: Optional[str] = Field(None, alias="name")
    address: Optional[str] = Field(None, alias="address")


class RenewalClause(BaseModel):
    notice_period: Optional[int] = Field(None, alias="Notice period")
    renewal_clause: Optional[str] = Field(None, alias="Renewal Clause")


class PerformancePenalty(BaseModel):
    condition: Optional[str] = Field(None, alias="condition")
    delivery: Optional[str] = Field(None, alias="delivery")
    penality: Optional[str] = Field(None, alias="penality")


class PricingValueCriteria(BaseModel):
    criteria: Optional[str] = Field(None, alias="Criteria")
    underlying_questions: Optional[str] = Field(None, alias="Underlying questions")
    rationale_for_assessment: Optional[str] = Field(None, alias="Rationale for Assessment")

class ContractDigest(BaseModel):
    parties_involved: Optional[str] = Field(None, alias="Parties involved")
    scope_of_work: Optional[str] = Field(None, alias="Scope of work")
    payment_terms: Optional[str] = Field(None, alias="Payment terms")
    termination_clause: Optional[str] = Field(None, alias="Termination clause")

class ExtractedEntities(BaseModel):
    buyer_termination_cause_period: Optional[int] = Field(None, alias="Buyer termination (cause) period")
    buyer_termination_convenience_period: Optional[int] = Field(None, alias="Buyer termination (convenience) period")
    contract_duration: Optional[int] = Field(None, alias="Contract duration")
    contract_expiry_date: Optional[str] = Field(None, alias="Contract expiry date")
    contract_start_date: Optional[str] = Field(None, alias="Contract start date")
    incoterms_shipping: Optional[str] = Field(None, alias="Incoterms/shipping")
    insurance: Optional[Insurance] = Field(None, alias="Insurance")
    jurisdiction_compliance: Optional[str] = Field(None, alias="Jurisdiction/compliance")
    payment_terms: Optional[PaymentTerms] = Field(None, alias="Payment terms")
    payment_invoicing_terms: Optional[PaymentInvoicingTerms] = Field(None, alias="Payment/invoicing terms")
    performance_penalties: Optional[List[PerformancePenalty]] = Field(None, alias="Performance penalties")
    prices: Optional[Prices] = Field(None, alias="Prices")
    renewal_clause_and_notice_period: Optional[RenewalClause] = Field(None, alias="Renewal clause and notice period")
    skus: Optional[List[SKUInfo]] = Field(None, alias="SKUs")
    specific_terms_agreed: Optional[Any] = Field(None, alias="Specific terms agreed")
    supplier: Optional[Any] = Field(None, alias="Supplier")
    region: Optional[str] = Field(None, alias="Region")
    contract_digest: Optional[ContractDigest] = Field(None, alias="Contract Digest")
    supplier_termination_convenience_period: Optional[int] = Field(None, alias="Supplier termination (convenience) period")
    title_for_the_contract: Optional[str] = Field(None, alias="Title for the contract")
    vendor_name_and_address_region: Optional[VendorInfo] = Field(None, alias="Vendor name and address/region")
    volume_commitment: Optional[Any] = Field(None, alias="Volume commitment")
    pricing_value_drivers_commercial_sustainability: Optional[List[PricingValueCriteria]] = Field(None, alias="Pricing Value, Drivers & Commercial Sustainability")
    partnership_contract_governance: Optional[List[str]] = Field(None, alias="Partnership & Contract Governance")

    class Config:
        populate_by_name = True
