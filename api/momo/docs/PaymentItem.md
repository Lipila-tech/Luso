# PaymentItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the payment Item | [optional] 
**item** | [**PaymentItemItem**](PaymentItemItem.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_item import PaymentItem

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentItem from a JSON string
payment_item_instance = PaymentItem.from_json(json)
# print the JSON string representation of the object
print(PaymentItem.to_json())

# convert the object into a dict
payment_item_dict = payment_item_instance.to_dict()
# create an instance of PaymentItem from a dict
payment_item_from_dict = PaymentItem.from_dict(payment_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


