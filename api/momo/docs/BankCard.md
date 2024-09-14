# BankCard

Detailed information for a bank card.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**brand** | **str** | Card brand. e.g. Visa, MasterCard, AmericanExpress. | [optional] 
**type** | **str** | Type of card. e.g. Credit, Debit. | [optional] 
**card_number** | **str** | Credit card number. | [optional] 
**expiration_date** | **datetime** | Expiration date of the card. | [optional] 
**cvv** | **str** | Security Code of the card. e.g. CCV, CCV2. | [optional] 
**last_four_digits** | **str** | Last four digits of the credit card. | [optional] 
**name_on_card** | **str** | Name on the card. | [optional] 
**bank** | **str** | Bank that issued the card. | [optional] 
**pin** | **str** | Customer pin created when tokenizing the card | [optional] 

## Example

```python
from openapi_client.models.bank_card import BankCard

# TODO update the JSON string below
json = "{}"
# create an instance of BankCard from a JSON string
bank_card_instance = BankCard.from_json(json)
# print the JSON string representation of the object
print(BankCard.to_json())

# convert the object into a dict
bank_card_dict = bank_card_instance.to_dict()
# create an instance of BankCard from a dict
bank_card_from_dict = BankCard.from_dict(bank_card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


