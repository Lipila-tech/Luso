# FeeRequestNotFound


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
from openapi_client.models.fee_request_not_found import FeeRequestNotFound

# TODO update the JSON string below
json = "{}"
# create an instance of FeeRequestNotFound from a JSON string
fee_request_not_found_instance = FeeRequestNotFound.from_json(json)
# print the JSON string representation of the object
print(FeeRequestNotFound.to_json())

# convert the object into a dict
fee_request_not_found_dict = fee_request_not_found_instance.to_dict()
# create an instance of FeeRequestNotFound from a dict
fee_request_not_found_from_dict = FeeRequestNotFound.from_dict(fee_request_not_found_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


