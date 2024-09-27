# coding: utf-8

"""
    Payments V1

    To facilitate the capability for consumers to make a payment or refund to service providers.

    The version of the OpenAPI document: v1.0
    Contact: developer-support@mtn.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from openapi_client.models.additional_info_object import AdditionalInfoObject
from openapi_client.models.details_object import DetailsObject
from openapi_client.models.payment_transaction_status_data import PaymentTransactionStatusData
from openapi_client.models.payment_transaction_status_response_links import PaymentTransactionStatusResponseLinks
from typing import Optional, Set
from typing_extensions import Self

class PaymentTransactionStatusResponse(BaseModel):
    """
    PaymentTransactionStatusResponse
    """ # noqa: E501
    status_code: Optional[StrictStr] = Field(default=None, description="This is the MADAPI Canonical Error Code (it is 4 characters long and it is not the HTTP Status Code which is 3 characters long). Back-end system errors are mapped to specific canonical error codes which are returned. 0000 is for a success. More information on these mappings can be found on the MADAPI Confluence Page 'Response Codes'", alias="statusCode")
    status_message: Optional[StrictStr] = Field(default=None, description="This is a description of the status", alias="statusMessage")
    correlator_id: Optional[StrictStr] = Field(default=None, description="Unique identifier in the client for the payment in case it is needed to correlate, a trace id associated with the caller", alias="correlatorId")
    customer_id: Optional[StrictStr] = Field(default=None, description="Customer identifier, a terminal id etc.", alias="customerId")
    sequence_no: Optional[StrictStr] = Field(default=None, description="A unique id for tracing all requests", alias="sequenceNo")
    provider_transaction_id: Optional[StrictStr] = Field(default=None, description="ID of the payment, generated by back-end system. This can be blank if the payment has previously been pre-approved.", alias="providerTransactionId")
    data: Optional[PaymentTransactionStatusData] = None
    additional_information: Optional[AdditionalInfoObject] = Field(default=None, alias="additionalInformation")
    details: Optional[DetailsObject] = None
    links: Optional[PaymentTransactionStatusResponseLinks] = Field(default=None, alias="_links")
    __properties: ClassVar[List[str]] = ["statusCode", "statusMessage", "correlatorId", "customerId", "sequenceNo", "providerTransactionId", "data", "additionalInformation", "details", "_links"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of PaymentTransactionStatusResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of data
        if self.data:
            _dict['data'] = self.data.to_dict()
        # override the default output from pydantic by calling `to_dict()` of additional_information
        if self.additional_information:
            _dict['additionalInformation'] = self.additional_information.to_dict()
        # override the default output from pydantic by calling `to_dict()` of details
        if self.details:
            _dict['details'] = self.details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of links
        if self.links:
            _dict['_links'] = self.links.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PaymentTransactionStatusResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "statusCode": obj.get("statusCode"),
            "statusMessage": obj.get("statusMessage"),
            "correlatorId": obj.get("correlatorId"),
            "customerId": obj.get("customerId"),
            "sequenceNo": obj.get("sequenceNo"),
            "providerTransactionId": obj.get("providerTransactionId"),
            "data": PaymentTransactionStatusData.from_dict(obj["data"]) if obj.get("data") is not None else None,
            "additionalInformation": AdditionalInfoObject.from_dict(obj["additionalInformation"]) if obj.get("additionalInformation") is not None else None,
            "details": DetailsObject.from_dict(obj["details"]) if obj.get("details") is not None else None,
            "_links": PaymentTransactionStatusResponseLinks.from_dict(obj["_links"]) if obj.get("_links") is not None else None
        })
        return _obj

