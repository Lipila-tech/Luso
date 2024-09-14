# TimePeriod

A period of time, either as a deadline (endDateTime only) a startDateTime only, or both

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end_date_time** | **datetime** | End of the time period, using IETC-RFC-3339 format | [optional] 
**start_date_time** | **datetime** | Start of the time period, using IETC-RFC-3339 format. If you define a start, you must also define an end | [optional] 

## Example

```python
from openapi_client.models.time_period import TimePeriod

# TODO update the JSON string below
json = "{}"
# create an instance of TimePeriod from a JSON string
time_period_instance = TimePeriod.from_json(json)
# print the JSON string representation of the object
print(TimePeriod.to_json())

# convert the object into a dict
time_period_dict = time_period_instance.to_dict()
# create an instance of TimePeriod from a dict
time_period_from_dict = TimePeriod.from_dict(time_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


