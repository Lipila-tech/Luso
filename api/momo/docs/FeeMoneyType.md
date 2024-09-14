# FeeMoneyType

Representation of SWZ monetary value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **float** | Amount of money | 
**units** | **str** | Currency | 

## Example

```python
from openapi_client.models.fee_money_type import FeeMoneyType

# TODO update the JSON string below
json = "{}"
# create an instance of FeeMoneyType from a JSON string
fee_money_type_instance = FeeMoneyType.from_json(json)
# print the JSON string representation of the object
print(FeeMoneyType.to_json())

# convert the object into a dict
fee_money_type_dict = fee_money_type_instance.to_dict()
# create an instance of FeeMoneyType from a dict
fee_money_type_from_dict = FeeMoneyType.from_dict(fee_money_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


