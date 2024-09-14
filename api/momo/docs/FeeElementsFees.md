# FeeElementsFees


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **str** | transfered amount | 
**units** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.fee_elements_fees import FeeElementsFees

# TODO update the JSON string below
json = "{}"
# create an instance of FeeElementsFees from a JSON string
fee_elements_fees_instance = FeeElementsFees.from_json(json)
# print the JSON string representation of the object
print(FeeElementsFees.to_json())

# convert the object into a dict
fee_elements_fees_dict = fee_elements_fees_instance.to_dict()
# create an instance of FeeElementsFees from a dict
fee_elements_fees_from_dict = FeeElementsFees.from_dict(fee_elements_fees_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


