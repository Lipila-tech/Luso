# BankAccountTransfer

Detailed information for a bank account transfer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_number** | **str** | Bank Account Number (this could refer to the IBAN or SWIFT number). | [optional] 
**account_number_type** | **str** | Type of account number. e.g. IBAN, SWIFT. | [optional] 
**bic** | **str** | Business Identifier Code/Swift code of the financial institution where the account is located. | [optional] 
**owner** | **str** | Owner of the bank account. | [optional] 
**bank** | **str** | Display nam of the bank. | [optional] 

## Example

```python
from openapi_client.models.bank_account_transfer import BankAccountTransfer

# TODO update the JSON string below
json = "{}"
# create an instance of BankAccountTransfer from a JSON string
bank_account_transfer_instance = BankAccountTransfer.from_json(json)
# print the JSON string representation of the object
print(BankAccountTransfer.to_json())

# convert the object into a dict
bank_account_transfer_dict = bank_account_transfer_instance.to_dict()
# create an instance of BankAccountTransfer from a dict
bank_account_transfer_from_dict = BankAccountTransfer.from_dict(bank_account_transfer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


