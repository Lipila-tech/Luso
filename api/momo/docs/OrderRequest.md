# OrderRequest

Order Request details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel** | **str** | Source system (Channel) identifier | [optional] 
**quote_id** | **str** | The ID of the quote used. | [optional] 
**description** | **str** | Text describing the contents of the payment. | [optional] 
**authentication_type** | **str** | This field will have the authentication type that the channel prefers to have for making a payment. Pass it as \&quot;Query Payment\&quot; incase if you don&#39;t need any back update notification about payment. Possible values are [Query Payment, Inline Auth, Notification] | [optional] 
**callback_url** | **str** | This field will have the call back URL to notify the payment status to the channels. This field should only be passed if authenticationType is Notification. The source channel initiating the order should give the notifyURL | [optional] 
**redirect_url** | **str** | This field will be the self service channel web page URL where the user is supposed to be once the payment is done on payportal | [optional] 
**delivery_method** | **str** | Method through which link need to be shared. In case of \&quot;SMS\&quot; URL is sent via SMS. In case of \&quot;Paylink\&quot; URL will be sent part of response. Possible values are [SMS, Payweb, Email, Paylink] | [optional] 
**payer** | [**Payer**](Payer.md) |  | [optional] 
**paymentmethods** | **List[str]** |  | [optional] 
**total_amount** | [**MoneyType**](MoneyType.md) |  | [optional] 
**item_details** | **List[object]** |  | [optional] 

## Example

```python
from openapi_client.models.order_request import OrderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of OrderRequest from a JSON string
order_request_instance = OrderRequest.from_json(json)
# print the JSON string representation of the object
print(OrderRequest.to_json())

# convert the object into a dict
order_request_dict = order_request_instance.to_dict()
# create an instance of OrderRequest from a dict
order_request_from_dict = OrderRequest.from_dict(order_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


