# PaymentMethodTypeDetails

Definition of the payment method. Its content depends on the type field.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bank_card** | [**BankCard**](BankCard.md) |  | [optional] 
**tokenized_card** | [**TokenizedCard**](TokenizedCard.md) |  | [optional] 
**bank_account_debit** | [**BankAccountDebit**](BankAccountDebit.md) |  | [optional] 
**bank_account_transfer** | [**BankAccountTransfer**](BankAccountTransfer.md) |  | [optional] 
**account** | [**Account**](Account.md) |  | [optional] 
**loyalty_account** | [**LoyaltyAccount**](LoyaltyAccount.md) |  | [optional] 
**bucket** | [**Bucket**](Bucket.md) |  | [optional] 
**voucher** | [**Voucher**](Voucher.md) |  | [optional] 
**digital_wallet** | [**DigitalWallet**](DigitalWallet.md) |  | [optional] 
**invoice** | [**InvoiceMethod**](InvoiceMethod.md) |  | [optional] 

## Example

```python
from openapi_client.models.payment_method_type_details import PaymentMethodTypeDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PaymentMethodTypeDetails from a JSON string
payment_method_type_details_instance = PaymentMethodTypeDetails.from_json(json)
# print the JSON string representation of the object
print(PaymentMethodTypeDetails.to_json())

# convert the object into a dict
payment_method_type_details_dict = payment_method_type_details_instance.to_dict()
# create an instance of PaymentMethodTypeDetails from a dict
payment_method_type_details_from_dict = PaymentMethodTypeDetails.from_dict(payment_method_type_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


