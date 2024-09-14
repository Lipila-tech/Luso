# PaymentResponseLinksSelf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**href** | **str** | Hyperlink to access the financial payment. | [optional] 

## Example

```python
from openapi_client.models.payment_response_links_self import PaymentResponseLinksSelf

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentResponseLinksSelf from a JSON string
payment_response_links_self_instance = PaymentResponseLinksSelf.from_json(json)
# print the JSON string representation of the object
print(PaymentResponseLinksSelf.to_json())

# convert the object into a dict
payment_response_links_self_dict = payment_response_links_self_instance.to_dict()
# create an instance of PaymentResponseLinksSelf from a dict
payment_response_links_self_from_dict = PaymentResponseLinksSelf.from_dict(payment_response_links_self_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


