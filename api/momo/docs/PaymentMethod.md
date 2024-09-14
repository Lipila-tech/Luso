# PaymentMethod

Reference or value of the method used to process the payment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Friendly name assigned to the payment method. | [optional] 
**description** | **str** | Description of the associated payment method. | [optional] 
**valid_from** | **datetime** | Period the payment method is valid. | [optional] 
**valid_to** | **datetime** | Period the payment method is valid. | [optional] 
**type** | [**PaymentMethodTypeEnum**](PaymentMethodTypeEnum.md) |  | 
**details** | [**PaymentMethodTypeDetails**](PaymentMethodTypeDetails.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_method import PaymentMethod

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethod from a JSON string
payment_method_instance = PaymentMethod.from_json(json)
# print the JSON string representation of the object
print(PaymentMethod.to_json())

# convert the object into a dict
payment_method_dict = payment_method_instance.to_dict()
# create an instance of PaymentMethod from a dict
payment_method_from_dict = PaymentMethod.from_dict(payment_method_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


