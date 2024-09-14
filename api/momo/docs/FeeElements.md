# FeeElements


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**quote_id** | **str** | 427842 | 
**fees** | [**FeeElementsFees**](FeeElementsFees.md) |  | 
**fee_fri** | **str** |  | 

## Example

```python
from openapi_client.models.fee_elements import FeeElements

# TODO update the JSON string below
json = "{}"
# create an instance of FeeElements from a JSON string
fee_elements_instance = FeeElements.from_json(json)
# print the JSON string representation of the object
print(FeeElements.to_json())

# convert the object into a dict
fee_elements_dict = fee_elements_instance.to_dict()
# create an instance of FeeElements from a dict
fee_elements_from_dict = FeeElements.from_dict(fee_elements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


