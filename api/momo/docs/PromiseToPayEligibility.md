# PromiseToPayEligibility

Payment Request eligibility details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eligibility_status** | **str** | Promise to pay eligibility status. Possible status values are ‘Eligible’, ‘Not-eligible’. | [optional] 
**account_balance** | **str** | Entire Outstanding amount of the account | [optional] 
**minimum_amount** | **str** | Applies NRT_THRESHOLD_VALUE on account balance and returns as the minimumAmount | [optional] 
**payment_start_date** | **str** | Payment Start Date holds API triggered date (DD-MM-YYYY) | [optional] 

## Example

```python
from openapi_client.models.promise_to_pay_eligibility import PromiseToPayEligibility

# TODO update the JSON string below
json = "{}"
# create an instance of PromiseToPayEligibility from a JSON string
promise_to_pay_eligibility_instance = PromiseToPayEligibility.from_json(json)
# print the JSON string representation of the object
print(PromiseToPayEligibility.to_json())

# convert the object into a dict
promise_to_pay_eligibility_dict = promise_to_pay_eligibility_instance.to_dict()
# create an instance of PromiseToPayEligibility from a dict
promise_to_pay_eligibility_from_dict = PromiseToPayEligibility.from_dict(promise_to_pay_eligibility_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


