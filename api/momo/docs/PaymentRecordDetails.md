# PaymentRecordDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**brand** | **str** |  | [optional] 
**issuer** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.payment_record_details import PaymentRecordDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentRecordDetails from a JSON string
payment_record_details_instance = PaymentRecordDetails.from_json(json)
# print the JSON string representation of the object
print(PaymentRecordDetails.to_json())

# convert the object into a dict
payment_record_details_dict = payment_record_details_instance.to_dict()
# create an instance of PaymentRecordDetails from a dict
payment_record_details_from_dict = PaymentRecordDetails.from_dict(payment_record_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


