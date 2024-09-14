# Bucket

Detailed information for a bucket that could be used to perform the payment, especially in the pre-paid environment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the bucket. | [optional] 
**name** | **str** | Entity name. | [optional] 
**description** | **str** | Description of the associated bucket. | [optional] 

## Example

```python
from openapi_client.models.bucket import Bucket

# TODO update the JSON string below
json = "{}"
# create an instance of Bucket from a JSON string
bucket_instance = Bucket.from_json(json)
# print the JSON string representation of the object
print(Bucket.to_json())

# convert the object into a dict
bucket_dict = bucket_instance.to_dict()
# create an instance of Bucket from a dict
bucket_from_dict = Bucket.from_dict(bucket_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


