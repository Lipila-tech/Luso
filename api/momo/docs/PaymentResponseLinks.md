# PaymentResponseLinks

Relevant links to the financial payment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | [**PaymentResponseLinksSelf**](PaymentResponseLinksSelf.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_response_links import PaymentResponseLinks

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentResponseLinks from a JSON string
payment_response_links_instance = PaymentResponseLinks.from_json(json)
# print the JSON string representation of the object
print(PaymentResponseLinks.to_json())

# convert the object into a dict
payment_response_links_dict = payment_response_links_instance.to_dict()
# create an instance of PaymentResponseLinks from a dict
payment_response_links_from_dict = PaymentResponseLinks.from_dict(payment_response_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


