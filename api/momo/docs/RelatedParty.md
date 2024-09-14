# RelatedParty

Related Entity reference. A related party defines party or party role linked to a specific entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of a related entity. | [optional] 
**name** | **str** | Name of the related entity. | [optional] 
**other_name** | **str** | Othername of the related party entity | [optional] 
**email** | **str** | Email of the related party entity | [optional] 
**valid_for** | [**TimePeriod**](TimePeriod.md) |  | [optional] 

## Example

```python
from openapi_client.models.related_party import RelatedParty

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedParty from a JSON string
related_party_instance = RelatedParty.from_json(json)
# print the JSON string representation of the object
print(RelatedParty.to_json())

# convert the object into a dict
related_party_dict = related_party_instance.to_dict()
# create an instance of RelatedParty from a dict
related_party_from_dict = RelatedParty.from_dict(related_party_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


