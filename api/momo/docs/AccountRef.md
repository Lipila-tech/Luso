# AccountRef


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the account | [optional] 
**description** | **str** | Detailed description of the account | [optional] 
**name** | **str** | Name of the account | [optional] 

## Example

```python
from openapi_client.models.account_ref import AccountRef

# TODO update the JSON string below
json = "{}"
# create an instance of AccountRef from a JSON string
account_ref_instance = AccountRef.from_json(json)
# print the JSON string representation of the object
print(AccountRef.to_json())

# convert the object into a dict
account_ref_dict = account_ref_instance.to_dict()
# create an instance of AccountRef from a dict
account_ref_from_dict = AccountRef.from_dict(account_ref_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


