# Money

A base / value business entity used to represent money

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit** | **str** | Currency (ISO4217 norm uses 3 letters to define the currency) | [optional] 
**value** | **float** | A positive floating point number | [optional] 

## Example

```python
from openapi_client.models.money import Money

# TODO update the JSON string below
json = "{}"
# create an instance of Money from a JSON string
money_instance = Money.from_json(json)
# print the JSON string representation of the object
print(Money.to_json())

# convert the object into a dict
money_dict = money_instance.to_dict()
# create an instance of Money from a dict
money_from_dict = Money.from_dict(money_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


