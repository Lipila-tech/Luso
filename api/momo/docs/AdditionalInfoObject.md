# AdditionalInfoObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Product Name. | [optional] 
**description** | **str** | Product Identifier. | [optional] 

## Example

```python
from openapi_client.models.additional_info_object import AdditionalInfoObject

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalInfoObject from a JSON string
additional_info_object_instance = AdditionalInfoObject.from_json(json)
# print the JSON string representation of the object
print(AdditionalInfoObject.to_json())

# convert the object into a dict
additional_info_object_dict = additional_info_object_instance.to_dict()
# create an instance of AdditionalInfoObject from a dict
additional_info_object_from_dict = AdditionalInfoObject.from_dict(additional_info_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


