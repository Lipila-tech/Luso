# PaymentTransactionStatusResponseLinks

Relevant links to the financial payment transaction status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | [**PaymentTransactionStatusResponseLinksSelf**](PaymentTransactionStatusResponseLinksSelf.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_transaction_status_response_links import PaymentTransactionStatusResponseLinks

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentTransactionStatusResponseLinks from a JSON string
payment_transaction_status_response_links_instance = PaymentTransactionStatusResponseLinks.from_json(json)
# print the JSON string representation of the object
print(PaymentTransactionStatusResponseLinks.to_json())

# convert the object into a dict
payment_transaction_status_response_links_dict = payment_transaction_status_response_links_instance.to_dict()
# create an instance of PaymentTransactionStatusResponseLinks from a dict
payment_transaction_status_response_links_from_dict = PaymentTransactionStatusResponseLinks.from_dict(payment_transaction_status_response_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


