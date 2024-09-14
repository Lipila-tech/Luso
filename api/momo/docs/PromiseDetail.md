# PromiseDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**installment_due_amount** | **str** | Installment Amount Due to be paid | [optional] 
**installment_end_date** | **datetime** | End date of Installment | [optional] 
**query_number** | **str** | Query Number in SV | [optional] 
**installment_start_date** | **datetime** | Start Date of Installment | [optional] 

## Example

```python
from openapi_client.models.promise_detail import PromiseDetail

# TODO update the JSON string below
json = "{}"
# create an instance of PromiseDetail from a JSON string
promise_detail_instance = PromiseDetail.from_json(json)
# print the JSON string representation of the object
print(PromiseDetail.to_json())

# convert the object into a dict
promise_detail_dict = promise_detail_instance.to_dict()
# create an instance of PromiseDetail from a dict
promise_detail_from_dict = PromiseDetail.from_dict(promise_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


