# DigitalWallet

Detailed information for a Digital Wallet.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service** | **str** | Organization, platform or currency backing the wallet. e.g. MoMo, PayPal, Yandex, BitCoin. Can also be an extension of a service being paid for | [optional] 
**wallet_id** | **str** | Account identifier in that service. | [optional] 
**wallet_uri** | **str** | URI pointing at the digital wallet. | [optional] 

## Example

```python
from openapi_client.models.digital_wallet import DigitalWallet

# TODO update the JSON string below
json = "{}"
# create an instance of DigitalWallet from a JSON string
digital_wallet_instance = DigitalWallet.from_json(json)
# print the JSON string representation of the object
print(DigitalWallet.to_json())

# convert the object into a dict
digital_wallet_dict = digital_wallet_instance.to_dict()
# create an instance of DigitalWallet from a dict
digital_wallet_from_dict = DigitalWallet.from_dict(digital_wallet_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


