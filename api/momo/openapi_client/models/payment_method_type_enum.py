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
import json
from enum import Enum
from typing_extensions import Self


class PaymentMethodTypeEnum(str, Enum):
    """
    PaymentMethodTypeEnum
    """

    """
    allowed enum values
    """
    BANKCARD = 'BankCard'
    TOKENIZEDCARD = 'TokenizedCard'
    BANKACCOUNTDEBIT = 'BankAccountDebit'
    BANKACCOUNTTRANSFER = 'BankAccountTransfer'
    ACCOUNT = 'Account'
    LOYALTYACCOUNT = 'LoyaltyAccount'
    BUCKET = 'Bucket'
    VOUCHER = 'Voucher'
    DIGITALWALLET = 'DigitalWallet'
    AIRTIME = 'Airtime'
    MOBILE_MONEY = 'Mobile Money'
    INVOICE = 'Invoice'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PaymentMethodTypeEnum from a JSON string"""
        return cls(json.loads(json_str))

