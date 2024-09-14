# ChargesObject

Total charges associated with a particular payment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **float** |  | [optional] 
**payer** | **str** | the bearer of the payment charges ie. [Merchant, Customer] | [optional] 

## Example

```python
from openapi_client.models.charges_object import ChargesObject

# TODO update the JSON string below
json = "{}"
# create an instance of ChargesObject from a JSON string
charges_object_instance = ChargesObject.from_json(json)
# print the JSON string representation of the object
print(ChargesObject.to_json())

# convert the object into a dict
charges_object_dict = charges_object_instance.to_dict()
# create an instance of ChargesObject from a dict
charges_object_from_dict = ChargesObject.from_dict(charges_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


