# PromiseToPayRequest

Payment Request details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**billing_account_no** | **str** | Unique Billing Account number of the customer | [optional] 
**service_name** | **str** | Service name of the payment. | [optional] 
**promise_open_date** | **datetime** | Start Date of the Promise. | [optional] 
**promise_amount** | **float** | Amount promised to be paid. | [optional] 
**number_of_installments** | **str** | Number of the EMI. | [optional] 
**duration_uom** | **str** | Unit of Measure for the EMI (can be Month, Week and Year). | [optional] 
**promise_threshold** | **str** | The Promise Threshold | [optional] 

## Example

```python
from openapi_client.models.promise_to_pay_request import PromiseToPayRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PromiseToPayRequest from a JSON string
promise_to_pay_request_instance = PromiseToPayRequest.from_json(json)
# print the JSON string representation of the object
print(PromiseToPayRequest.to_json())

# convert the object into a dict
promise_to_pay_request_dict = promise_to_pay_request_instance.to_dict()
# create an instance of PromiseToPayRequest from a dict
promise_to_pay_request_from_dict = PromiseToPayRequest.from_dict(promise_to_pay_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


