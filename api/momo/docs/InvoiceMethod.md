# InvoiceMethod

Detailed information for an invoice

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | This is the Id of the invoice | [optional] 
**type** | **str** | Type of the invoice being paid for | [optional] 
**frequency** | **str** | This is the frequency of a reccuring transaction | [optional] 
**start_date** | **str** | This is the start date of a reccuring transaction | [optional] 
**end_date** | **str** | This is the end date of a reccuring transaction | [optional] 
**retry_on_fail** | **bool** | A boolean to showing if the transaction should be retried on fail or not. | [optional] 
**deactivate_on_fail** | **str** | A boolean to showing if the transaction should be deactivated on fail or not. | [optional] 
**callback_url** | **str** | The url to be invoked for callbacks | [optional] 
**retry_run** | **str** | This is the retry run | [optional] 
**retry_frequency** | **str** | The retry frequencies | [optional] 

## Example

```python
from openapi_client.models.invoice_method import InvoiceMethod

# TODO update the JSON string below
json = "{}"
# create an instance of InvoiceMethod from a JSON string
invoice_method_instance = InvoiceMethod.from_json(json)
# print the JSON string representation of the object
print(InvoiceMethod.to_json())

# convert the object into a dict
invoice_method_dict = invoice_method_instance.to_dict()
# create an instance of InvoiceMethod from a dict
invoice_method_from_dict = InvoiceMethod.from_dict(invoice_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


