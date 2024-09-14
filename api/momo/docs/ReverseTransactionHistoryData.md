# ReverseTransactionHistoryData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transactionstatus** | **str** | SUCCESSFULL. | [optional] 
**transfertype** | **str** | TRANSFER. | [optional] 
**startdate** | **str** | Select transactions starting from this date and time. | [optional] 
**commitdate** | **str** | The date and time at which the transaction was completed. | [optional] 
**fxrate** | **str** | The foreign exchange rate. | [optional] 
**externalfxrate** | **str** | The external foreign exchange rate in an interoperability transfer. | [optional] 
**initiatinguser** | **str** | The execution ID of the user that initiated the transaction. | [optional] 
**realuser** | **str** | The execution ID of the real user that initiated the transaction. | [optional] 
**reviewinguser** | **str** | The execution ID of the user that reviewed the transaction. | [optional] 
**initiatingaccountholder** | **str** | The Identity of the account holder that initiated the transaction if it was initiated by an account holder. | [optional] 
**realaccountholder** | **str** | The Identity of the real account holder that is effected by the transaction if it was initiated by an account holder. | [optional] 
**providercategory** | **str** | The name of the provider category. | [optional] 
**var_from** | **str** | The sending user&#39;s default FRI. | [optional] 
**fromaccount** | **str** | The sending account FRI. | [optional] 
**fromamount** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromfee** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromexternalfee** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromdiscount** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**frompromotion** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromloyfee** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromloyreward** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**frompromotionrefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromnote** | **str** | The sender&#39;s note.. | [optional] 
**fromavailablebalance** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromtotalbalance** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromcommittedbalance** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromaccountholder** | **str** | The identity of the sending account holder. | [optional] 
**originalamount** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**externalamount** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**amount** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromcouponvalue** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromtaxes** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromtaxesrefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**to** | **str** | The receiving user&#39;s FRI or the receiving account&#39;s FRI. | [optional] 
**toaccount** | **str** | The receiving account&#39;s FRI. | [optional] 
**toamount** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**tofee** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**toexternalfee** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**topromotion** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**toloyfee** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**toloyreward** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**topromotionrefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**todiscountrefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**tomessage** | **str** | The receiver&#39;s message. | [optional] 
**toavailablebalance** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**tototalbalance** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**tocommittedbalance** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**maininstructionid** | **str** | The main instruction ID. | [optional] 
**instructionid** | **str** | The financial instruction ID.. | [optional] 
**externaltransactionid** | **str** | External transaction ID for the operation.. | [optional] 
**transactiontext** | **str** | Text describing the transaction.. | [optional] 
**tofeerefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromfeerefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**toaccountholder** | **str** | The Identity of the receiving account holder. | [optional] 
**totaxes** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**totaxesrefund** | [**MoneyCurrencyType**](MoneyCurrencyType.md) |  | [optional] 
**fromfirstname** | **str** | The first name of the sender. | [optional] 
**fromlastname** | **str** | The last name of the sender. | [optional] 
**fromhandlerfirstname** | **str** | The first name of the handler on the sender side. | [optional] 
**fromhandlerlastname** | **str** | The last name of the handler on the sender side. | [optional] 
**tofirstname** | **str** | The first name of receiver. | [optional] 
**tolastname** | **str** | The last name of the receiver. | [optional] 
**tohandlerfirstname** | **str** | The first name of the handler on the receiver side. | [optional] 
**tohandlerlastname** | **str** | The last name of the handler on the receiver side. | [optional] 
**fromposmsisdn** | **str** | The point of sale msisdn of the sender. | [optional] 
**toposmsisdn** | **str** | The point of sale msisdn of the receiver. | [optional] 
**originaltransactionid** | **str** | The original transaction id.. | [optional] 
**communicationchannel** | **str** | The communication channel.. | [optional] 
**externalserviceprovider** | **str** | The external service provider that was involved in the transaction.. | [optional] 
**external_svc_prd_tran_id** | **str** | The transaction ID generated by an external service provider. This field is only available when searching for a specific transaction by financialTransactionId or externalTransactionId. | [optional] 
**from_ex_instru_prov_trans_id** | **str** | The external transaction identifier as provided by the external instrument provider if the sending FRI is an external instrument. This field is only available when searching for a specific transaction by financialTransactionId or externalTransactionId.. | [optional] 
**to_ex_instru_prov_trans_id** | **str** | The external transaction identifier as provided by the external instrument provider if the receiving FRI is an external instrument. This field is only available when searching for a specific transaction by financialTransactionId or externalTransactionId. | [optional] 
**from_ex_instru_acc_holder** | **str** | The external instrument provider account holder if the sending FRI is an external instrument. This field is only available when searching for a specific transaction by financialTransactionId or externalTransactionId. | [optional] 
**to_ex_instru_acc_holder** | **str** | The external instrument provider account holder if the receiving FRI is an external instrument. This field is only available when searching for a specific transaction by financialTransactionId or externalTransactionId. | [optional] 
**fitype** | **str** | Shows the financial transaction type. | [optional] 

## Example

```python
from openapi_client.models.reverse_transaction_history_data import ReverseTransactionHistoryData

# TODO update the JSON string below
json = "{}"
# create an instance of ReverseTransactionHistoryData from a JSON string
reverse_transaction_history_data_instance = ReverseTransactionHistoryData.from_json(json)
# print the JSON string representation of the object
print(ReverseTransactionHistoryData.to_json())

# convert the object into a dict
reverse_transaction_history_data_dict = reverse_transaction_history_data_instance.to_dict()
# create an instance of ReverseTransactionHistoryData from a dict
reverse_transaction_history_data_from_dict = ReverseTransactionHistoryData.from_dict(reverse_transaction_history_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


