# DetailsObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**brand** | **str** | Telco Code. | [optional] 
**fulfillment_msisdn** | **str** | Fulfillment Msisdn. | [optional] 
**issuer** | **str** | Source of funds scheme. | [optional] 

## Example

```python
from openapi_client.models.details_object import DetailsObject

# TODO update the JSON string below
json = "{}"
# create an instance of DetailsObject from a JSON string
details_object_instance = DetailsObject.from_json(json)
# print the JSON string representation of the object
print(DetailsObject.to_json())

# convert the object into a dict
details_object_dict = details_object_instance.to_dict()
# create an instance of DetailsObject from a dict
details_object_from_dict = DetailsObject.from_dict(details_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


