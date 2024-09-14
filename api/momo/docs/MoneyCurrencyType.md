# MoneyCurrencyType

Representation of monetary value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **float** | Amount of money | 
**currency** | **str** | Currency | 

## Example

```python
from openapi_client.models.money_currency_type import MoneyCurrencyType

# TODO update the JSON string below
json = "{}"
# create an instance of MoneyCurrencyType from a JSON string
money_currency_type_instance = MoneyCurrencyType.from_json(json)
# print the JSON string representation of the object
print(MoneyCurrencyType.to_json())

# convert the object into a dict
money_currency_type_dict = money_currency_type_instance.to_dict()
# create an instance of MoneyCurrencyType from a dict
money_currency_type_from_dict = MoneyCurrencyType.from_dict(money_currency_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


