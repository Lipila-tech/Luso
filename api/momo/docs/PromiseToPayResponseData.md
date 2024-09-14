# PromiseToPayResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**promise_details** | [**List[PromiseDetail]**](PromiseDetail.md) |  | [optional] 

## Example

```python
from openapi_client.models.promise_to_pay_response_data import PromiseToPayResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of PromiseToPayResponseData from a JSON string
promise_to_pay_response_data_instance = PromiseToPayResponseData.from_json(json)
# print the JSON string representation of the object
print(PromiseToPayResponseData.to_json())

# convert the object into a dict
promise_to_pay_response_data_dict = promise_to_pay_response_data_instance.to_dict()
# create an instance of PromiseToPayResponseData from a dict
promise_to_pay_response_data_from_dict = PromiseToPayResponseData.from_dict(promise_to_pay_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


