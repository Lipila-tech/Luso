# LoyaltyAccount

Detailed information for a loyalty system that could be used to perform the payment..

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the loyalty account. | [optional] 
**name** | **str** | Entity name. | [optional] 
**description** | **str** | Description of the associated loyalty account. | [optional] 

## Example

```python
from openapi_client.models.loyalty_account import LoyaltyAccount

# TODO update the JSON string below
json = "{}"
# create an instance of LoyaltyAccount from a JSON string
loyalty_account_instance = LoyaltyAccount.from_json(json)
# print the JSON string representation of the object
print(LoyaltyAccount.to_json())

# convert the object into a dict
loyalty_account_dict = loyalty_account_instance.to_dict()
# create an instance of LoyaltyAccount from a dict
loyalty_account_from_dict = LoyaltyAccount.from_dict(loyalty_account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


