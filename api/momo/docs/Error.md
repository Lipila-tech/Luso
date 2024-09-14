# Error


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **str** | This is the MADAPI Canonical Error Code (it is 4 characters long and it is not the HTTP Status Code which is 3 characters long). Back-end system errors are mapped to specific canonical error codes which are returned. More information on these mappings can be found on the MADAPI Confluence Page &#39;Response Codes&#39; | 
**status_message** | **str** | More details and corrective actions related to the error which can be shown to a client | 
**support_message** | **str** | Internal message meant for consumers of the API to troubleshoot the error (could possible include the back-end system error code in the message if it would be useful) | [optional] 
**transaction_id** | **str** | This is the same transactionId that is sent in the request | [optional] 
**timestamp** | **datetime** | Timestamp that the error occurred | [optional] 
**sequence_no** | **str** | A unique id for tracing all requests | [optional] 
**path** | **str** | The path that caused the error | [optional] 
**method** | **str** | The HTTP method type that was used | [optional] 

## Example

```python
from openapi_client.models.error import Error

# TODO update the JSON string below
json = "{}"
# create an instance of Error from a JSON string
error_instance = Error.from_json(json)
# print the JSON string representation of the object
print(Error.to_json())

# convert the object into a dict
error_dict = error_instance.to_dict()
# create an instance of Error from a dict
error_from_dict = Error.from_dict(error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


