# ReverseTransactionHistory


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **str** |  | [optional] 
**status_message** | **str** |  | [optional] 
**transaction_id** | **str** | API generated Id to include for tracing requests | [optional] 
**correlator_id** | **str** |  | [optional] 
**sequence_no** | **str** | A unique id for tracing all requests | [optional] 
**data** | [**ReverseTransactionHistoryData**](ReverseTransactionHistoryData.md) |  | [optional] 
**loyalty_information** | [**LoyaltyBalances**](LoyaltyBalances.md) |  | [optional] 
**links** | [**PaymentResponseLinks**](PaymentResponseLinks.md) |  | [optional] 

## Example

```python
from openapi_client.models.reverse_transaction_history import ReverseTransactionHistory

# TODO update the JSON string below
json = "{}"
# create an instance of ReverseTransactionHistory from a JSON string
reverse_transaction_history_instance = ReverseTransactionHistory.from_json(json)
# print the JSON string representation of the object
print(ReverseTransactionHistory.to_json())

# convert the object into a dict
reverse_transaction_history_dict = reverse_transaction_history_instance.to_dict()
# create an instance of ReverseTransactionHistory from a dict
reverse_transaction_history_from_dict = ReverseTransactionHistory.from_dict(reverse_transaction_history_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


