# AdditionalInformation

Additional information relating to the payment transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of additional information item. | 
**description** | **str** | Description of additional information item. | 

## Example

```python
from openapi_client.models.additional_information import AdditionalInformation

# TODO update the JSON string below
json = "{}"
# create an instance of AdditionalInformation from a JSON string
additional_information_instance = AdditionalInformation.from_json(json)
# print the JSON string representation of the object
print(AdditionalInformation.to_json())

# convert the object into a dict
additional_information_dict = additional_information_instance.to_dict()
# create an instance of AdditionalInformation from a dict
additional_information_from_dict = AdditionalInformation.from_dict(additional_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


