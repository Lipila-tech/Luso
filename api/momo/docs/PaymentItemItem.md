# PaymentItemItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID of the item being paid for. This can be a productId | [optional] 
**name** | **str** | This is the name of the item being paid for | [optional] 

## Example

```python
from openapi_client.models.payment_item_item import PaymentItemItem

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentItemItem from a JSON string
payment_item_item_instance = PaymentItemItem.from_json(json)
# print the JSON string representation of the object
print(PaymentItemItem.to_json())

# convert the object into a dict
payment_item_item_dict = payment_item_item_instance.to_dict()
# create an instance of PaymentItemItem from a dict
payment_item_item_from_dict = PaymentItemItem.from_dict(payment_item_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


