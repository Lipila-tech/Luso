# FeecheckRequest

Payment Request details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**correlator_id** | **str** | Unique identifier in the client for the payment in case it is needed to correlate, a trace id associated with the caller | 
**payment_date** | **datetime** | Date when the payment was performed. | [optional] 
**name** | **str** | Screen name of the payment. | [optional] 
**calling_system** | **str** | calling system. | [optional] 
**transaction_type** | **str** | calling systemn. | 
**target_system** | **str** | calling systemn. | [optional] 
**callback_url** | **str** | The callback URL. | 
**quote_id** | **str** | The ID of the quote used, a terminal id associated with the caller. | [optional] 
**channel** | **str** | The channel used to perform the payment operation or just the channel itself with just its name. | [optional] 
**description** | **str** | Text describing the contents of the payment. | [optional] 
**authorization_code** | **str** | Authorization code retrieved from an external payment gateway that could be used for conciliation. | [optional] 
**fee_bearer** | **str** | Who bears a charge for a particular transaction , whether a Payer or Payee | [optional] 
**amount** | [**FeeMoneyType**](FeeMoneyType.md) |  | [optional] 
**tax_amount** | [**FeeMoneyType**](FeeMoneyType.md) |  | [optional] 
**total_amount** | [**FeeMoneyType**](FeeMoneyType.md) |  | 
**payer** | [**Payer**](Payer.md) |  | [optional] 
**payee** | [**List[Payee]**](Payee.md) |  | [optional] 
**payment_method** | [**PaymentMethod**](PaymentMethod.md) |  | 
**status** | **str** | Status of the payment method. | [optional] 
**status_date** | **datetime** | Time the status of the payment method changed. | [optional] 
**additional_information** | [**List[AdditionalInformation]**](AdditionalInformation.md) |  | [optional] 
**segment** | **str** | Segment of the customer. Forexample, subscriber,agent, merchant, admin depending on the type of customer whome the operation is being performed against. | [optional] 

## Example

```python
from openapi_client.models.feecheck_request import FeecheckRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FeecheckRequest from a JSON string
feecheck_request_instance = FeecheckRequest.from_json(json)
# print the JSON string representation of the object
print(FeecheckRequest.to_json())

# convert the object into a dict
feecheck_request_dict = feecheck_request_instance.to_dict()
# create an instance of FeecheckRequest from a dict
feecheck_request_from_dict = FeecheckRequest.from_dict(feecheck_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


