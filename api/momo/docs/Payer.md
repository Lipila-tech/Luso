# Payer

The individual that performs the payment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payer_id_type** | **str** | Identifier Type of the Payer. | [optional] 
**payer_id** | **str** | The Payer identifier, can be a sending fri, an msisdn etc. | 
**payer_note** | **str** | A descriptive note for sender transaction history,ex. a sender note | [optional] 
**payer_name** | **str** | Name of the payer | [optional] 
**payer_email** | **str** | An optional email address of the payer or customer | [optional] 
**payer_ref** | **str** | A reference to the payer | [optional] 
**payer_surname** | **str** | Surname of the payer | [optional] 
**include_payer_charges** | **bool** | A boolean value to add payment charges | [optional] 

## Example

```python
from openapi_client.models.payer import Payer

# TODO update the JSON string below
json = "{}"
# create an instance of Payer from a JSON string
payer_instance = Payer.from_json(json)
# print the JSON string representation of the object
print(Payer.to_json())

# convert the object into a dict
payer_dict = payer_instance.to_dict()
# create an instance of Payer from a dict
payer_from_dict = Payer.from_dict(payer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


