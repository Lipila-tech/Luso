# InboundResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **str** | This is the MADAPI Canonical Error Code (it is 4 characters long and it is not the HTTP Status Code which is 3 characters long). Back-end system errors are mapped to specific canonical error codes which are returned. 0000 is for a success. More information on these mappings can be found on the MADAPI Confluence Page &#39;Response Codes&#39;  | 
**error** | **str** |  | 
**sequence_no** | **str** | A unique id for tracing all requests | [optional] 
**data** | [**InboundResponseData**](InboundResponseData.md) |  | 

## Example

```python
from openapi_client.models.inbound_response import InboundResponse

# TODO update the JSON string below
json = "{}"
# create an instance of InboundResponse from a JSON string
inbound_response_instance = InboundResponse.from_json(json)
# print the JSON string representation of the object
print(InboundResponse.to_json())

# convert the object into a dict
inbound_response_dict = inbound_response_instance.to_dict()
# create an instance of InboundResponse from a dict
inbound_response_from_dict = InboundResponse.from_dict(inbound_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


