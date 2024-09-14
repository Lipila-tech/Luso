# PaymentRecord


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payment_date** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**fulfillment_status** | **str** |  | [optional] 
**details** | [**PaymentRecordDetails**](PaymentRecordDetails.md) |  | [optional] 
**payment_id** | **str** |  | [optional] 
**payment_type** | **str** |  | [optional] 
**commit_date** | **str** |  | [optional] 
**fx_rate** | **str** |  | [optional] 
**initiating_user** | **str** |  | [optional] 
**real_user** | **str** |  | [optional] 
**initiating_account_holder** | **str** |  | [optional] 
**real_account_holder** | **str** |  | [optional] 
**originator** | **str** |  | [optional] 
**originator_account** | **str** |  | [optional] 
**main_instruction_id** | **str** |  | [optional] 
**instruction_id** | **str** |  | [optional] 
**transaction_id** | **str** |  | [optional] 
**destination_account_holder** | **str** |  | [optional] 
**originator_first_name** | **str** |  | [optional] 
**originator_last_name** | **str** |  | [optional] 
**originator_handler_first_name** | **str** |  | [optional] 
**originator_handler_last_name** | **str** |  | [optional] 
**destination_first_name** | **str** |  | [optional] 
**destination_last_name** | **str** |  | [optional] 
**destination_handler_first_name** | **str** |  | [optional] 
**destination_handler_last_name** | **str** |  | [optional] 
**channel** | **str** |  | [optional] 
**originator_account_holder** | **str** |  | [optional] 
**destination** | **str** |  | [optional] 
**destination_account** | **str** |  | [optional] 
**originator_amount** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**originator_fee** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**original_amount** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**amount** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**destination_amount** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**destination_fee** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**destination_available_balance** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**destination_total_balance** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 
**destination_committed_balance** | [**PaymentRecordOriginatorAmount**](PaymentRecordOriginatorAmount.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_record import PaymentRecord

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentRecord from a JSON string
payment_record_instance = PaymentRecord.from_json(json)
# print the JSON string representation of the object
print(PaymentRecord.to_json())

# convert the object into a dict
payment_record_dict = payment_record_instance.to_dict()
# create an instance of PaymentRecord from a dict
payment_record_from_dict = PaymentRecord.from_dict(payment_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


