# PaymentHistoryResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of Payment | [optional] 
**href** | **str** | Hypertext Reference of the Payment | [optional] 
**authorization_code** | **str** | Authorization code retrieved from an external payment gateway that could be used for conciliation | [optional] 
**correlator_id** | **str** | Unique identifier in the client for the payment in case it is needed to correlate | [optional] 
**description** | **str** | Text describing the contents of the payment | [optional] 
**name** | **str** | Screen name of the payment | [optional] 
**payment_date** | **datetime** | Date when the payment was performed | [optional] 
**status** | **str** | Status of the payment | [optional] 
**status_date** | **datetime** | Date when the status was recorded | [optional] 
**account** | [**AccountRef**](AccountRef.md) |  | [optional] 
**amount** | [**Money**](Money.md) |  | [optional] 
**related_party** | [**RelatedParty**](RelatedParty.md) |  | [optional] 
**payer** | [**RelatedParty**](RelatedParty.md) |  | [optional] 
**payment_item** | [**List[PaymentItem]**](PaymentItem.md) |  | [optional] 
**total_amount** | [**Money**](Money.md) |  | [optional] 
**type** | **str** | When sub-classing, this defines the sub-class entity name | [optional] 
**callback_url** | **str** | Callback URL | [optional] 
**payment_records** | [**List[PaymentRecord]**](PaymentRecord.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_history_response_data import PaymentHistoryResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentHistoryResponseData from a JSON string
payment_history_response_data_instance = PaymentHistoryResponseData.from_json(json)
# print the JSON string representation of the object
print(PaymentHistoryResponseData.to_json())

# convert the object into a dict
payment_history_response_data_dict = payment_history_response_data_instance.to_dict()
# create an instance of PaymentHistoryResponseData from a dict
payment_history_response_data_from_dict = PaymentHistoryResponseData.from_dict(payment_history_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


