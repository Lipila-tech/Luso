# PromiseToPayResponse

Promise details response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **str** | This is the MADAPI Canonical Error Code (it is 4 characters long and it is not the HTTP Status Code which is 3 characters long). Back-end system errors are mapped to specific canonical error codes which are returned. 0000 is for a success. More information on these mappings can be found on the MADAPI Confluence Page &#39;Response Codes&#39; | [optional] 
**status_message** | **str** | Message of the transaction. Either Success or Failure. | [optional] 
**transaction_id** | **str** | Unique identifier for every request to the backend. Mapped from input request. | [optional] 
**sequence_no** | **str** | A unique id for tracing all requests | [optional] 
**data** | [**PromiseToPayResponseData**](PromiseToPayResponseData.md) |  | [optional] 
**links** | [**ResponseLinks**](ResponseLinks.md) |  | [optional] 

## Example

```python
from openapi_client.models.promise_to_pay_response import PromiseToPayResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PromiseToPayResponse from a JSON string
promise_to_pay_response_instance = PromiseToPayResponse.from_json(json)
# print the JSON string representation of the object
print(PromiseToPayResponse.to_json())

# convert the object into a dict
promise_to_pay_response_dict = promise_to_pay_response_instance.to_dict()
# create an instance of PromiseToPayResponse from a dict
promise_to_pay_response_from_dict = PromiseToPayResponse.from_dict(promise_to_pay_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


