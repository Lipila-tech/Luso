# Payee

A payment can be made in the context of an order, a recharge, for ongoing bills, for administrative fee (e.g. re-sending a paper copy of a bill), damaged device penalty, and more.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | [**MoneyType**](MoneyType.md) |  | [optional] 
**tax_amount** | [**MoneyType**](MoneyType.md) |  | [optional] 
**total_amount** | [**MoneyType**](MoneyType.md) |  | 
**payee_id_type** | **str** | Identifier Type of the Payee. | [optional] 
**payee_id** | **str** | The Payee identifier, ie. can be a receivingfri or a merchant Id etc. | [optional] 
**payee_note** | **str** | A descriptive note for receiver transaction history, ie. a receiver message | [optional] 
**payee_name** | **str** | Name of the payee | [optional] 

## Example

```python
from openapi_client.models.payee import Payee

# TODO update the JSON string below
json = "{}"
# create an instance of Payee from a JSON string
payee_instance = Payee.from_json(json)
# print the JSON string representation of the object
print(Payee.to_json())

# convert the object into a dict
payee_dict = payee_instance.to_dict()
# create an instance of Payee from a dict
payee_from_dict = Payee.from_dict(payee_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


