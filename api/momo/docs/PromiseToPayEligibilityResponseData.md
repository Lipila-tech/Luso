# PromiseToPayEligibilityResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**promise_to_pay_eligibility_details** | [**PromiseToPayEligibility**](PromiseToPayEligibility.md) |  | [optional] 

## Example

```python
from openapi_client.models.promise_to_pay_eligibility_response_data import PromiseToPayEligibilityResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of PromiseToPayEligibilityResponseData from a JSON string
promise_to_pay_eligibility_response_data_instance = PromiseToPayEligibilityResponseData.from_json(json)
# print the JSON string representation of the object
print(PromiseToPayEligibilityResponseData.to_json())

# convert the object into a dict
promise_to_pay_eligibility_response_data_dict = promise_to_pay_eligibility_response_data_instance.to_dict()
# create an instance of PromiseToPayEligibilityResponseData from a dict
promise_to_pay_eligibility_response_data_from_dict = PromiseToPayEligibilityResponseData.from_dict(promise_to_pay_eligibility_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


