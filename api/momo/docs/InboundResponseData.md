# InboundResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **str** | message | [optional] 
**provider_transaction_id** | **str** |  | [optional] 
**status_message** | **str** |  | [optional] 
**fee_details** | [**List[FeeElements]**](FeeElements.md) |  | [optional] 

## Example

```python
from openapi_client.models.inbound_response_data import InboundResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of InboundResponseData from a JSON string
inbound_response_data_instance = InboundResponseData.from_json(json)
# print the JSON string representation of the object
print(InboundResponseData.to_json())

# convert the object into a dict
inbound_response_data_dict = inbound_response_data_instance.to_dict()
# create an instance of InboundResponseData from a dict
inbound_response_data_from_dict = InboundResponseData.from_dict(inbound_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


