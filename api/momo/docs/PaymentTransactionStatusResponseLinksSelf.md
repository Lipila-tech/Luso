# PaymentTransactionStatusResponseLinksSelf


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**href** | **str** | Hyperlink to access the financial payment transaction status. | [optional] 

## Example

```python
from openapi_client.models.payment_transaction_status_response_links_self import PaymentTransactionStatusResponseLinksSelf

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentTransactionStatusResponseLinksSelf from a JSON string
payment_transaction_status_response_links_self_instance = PaymentTransactionStatusResponseLinksSelf.from_json(json)
# print the JSON string representation of the object
print(PaymentTransactionStatusResponseLinksSelf.to_json())

# convert the object into a dict
payment_transaction_status_response_links_self_dict = payment_transaction_status_response_links_self_instance.to_dict()
# create an instance of PaymentTransactionStatusResponseLinksSelf from a dict
payment_transaction_status_response_links_self_from_dict = PaymentTransactionStatusResponseLinksSelf.from_dict(payment_transaction_status_response_links_self_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


