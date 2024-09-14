# BadFeeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **datetime** | Timestamp that the error occurred | [optional] 
**status** | **str** | Http status | [optional] 
**error** | **str** | error message | [optional] 
**message** | **str** | error message | [optional] 
**sequence_no** | **str** | A unique id for tracing all requests | [optional] 
**path** | **str** | The path that caused the error | [optional] 

## Example

```python
from openapi_client.models.bad_fee_request import BadFeeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BadFeeRequest from a JSON string
bad_fee_request_instance = BadFeeRequest.from_json(json)
# print the JSON string representation of the object
print(BadFeeRequest.to_json())

# convert the object into a dict
bad_fee_request_dict = bad_fee_request_instance.to_dict()
# create an instance of BadFeeRequest from a dict
bad_fee_request_from_dict = BadFeeRequest.from_dict(bad_fee_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


