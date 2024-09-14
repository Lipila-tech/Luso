# PaymentHistoryResponse

The Payment resource represents a performed payment. It contains both information about the payment and the payment method used to perform it.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **str** | This is the MADAPI Canonical Error Code (it is 4 characters long and it is not the HTTP Status Code which is 3 characters long). Back-end system errors are mapped to specific canonical error codes which are returned. 0000 is for a success. More information on these mappings can be found on the MADAPI Confluence Page &#39;Response Codes&#39; | [optional] 
**status_message** | **str** | Message of the transaction. Either Success or Failure. | [optional] 
**transaction_id** | **str** | Unique identifier for every request to the backend. Mapped from input request. | [optional] 
**customer_id** | **str** | Customer Id of the customer whose history is being retrieved | [optional] 
**sequence_no** | **str** | A unique id for tracing all requests | [optional] 
**data** | [**PaymentHistoryResponseData**](PaymentHistoryResponseData.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_history_response import PaymentHistoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentHistoryResponse from a JSON string
payment_history_response_instance = PaymentHistoryResponse.from_json(json)
# print the JSON string representation of the object
print(PaymentHistoryResponse.to_json())

# convert the object into a dict
payment_history_response_dict = payment_history_response_instance.to_dict()
# create an instance of PaymentHistoryResponse from a dict
payment_history_response_from_dict = PaymentHistoryResponse.from_dict(payment_history_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


