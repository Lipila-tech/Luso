# CustomerObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firstname** | **str** | Customer First Name. | [optional] 
**surname** | **str** | Customer surname. | [optional] 
**email** | **str** | Customer email. | [optional] 
**msisdn** | **str** | Customer Mobile number. | [optional] 

## Example

```python
from openapi_client.models.customer_object import CustomerObject

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerObject from a JSON string
customer_object_instance = CustomerObject.from_json(json)
# print the JSON string representation of the object
print(CustomerObject.to_json())

# convert the object into a dict
customer_object_dict = customer_object_instance.to_dict()
# create an instance of CustomerObject from a dict
customer_object_from_dict = CustomerObject.from_dict(customer_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


