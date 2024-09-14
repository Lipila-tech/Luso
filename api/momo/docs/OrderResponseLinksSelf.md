# OrderResponseLinksSelf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**href** | **str** | Hyperlink to access the payment link generation endpoint. | [optional] 

## Example

```python
from openapi_client.models.order_response_links_self import OrderResponseLinksSelf

# TODO update the JSON string below
json = "{}"
# create an instance of OrderResponseLinksSelf from a JSON string
order_response_links_self_instance = OrderResponseLinksSelf.from_json(json)
# print the JSON string representation of the object
print(OrderResponseLinksSelf.to_json())

# convert the object into a dict
order_response_links_self_dict = order_response_links_self_instance.to_dict()
# create an instance of OrderResponseLinksSelf from a dict
order_response_links_self_from_dict = OrderResponseLinksSelf.from_dict(order_response_links_self_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


