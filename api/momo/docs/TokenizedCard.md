# TokenizedCard

Detailed information for a stored tokenized card.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**brand** | **str** | Card brand. Might be used for display purposes. | [optional] 
**type** | **str** | Card type. Might be used for display purposes. | [optional] 
**last_four_digits** | **str** | Last four digits of the credit card or a token authentication PIN. Might be used for display purposes. | [optional] 
**token_type** | **str** | Token type. e.g emv. | [optional] 
**token** | **str** | The token itself ie. a token id associated with a the payment card. | [optional] 
**issuer** | **str** | Whoever issued the token. | [optional] 

## Example

```python
from openapi_client.models.tokenized_card import TokenizedCard

# TODO update the JSON string below
json = "{}"
# create an instance of TokenizedCard from a JSON string
tokenized_card_instance = TokenizedCard.from_json(json)
# print the JSON string representation of the object
print(TokenizedCard.to_json())

# convert the object into a dict
tokenized_card_dict = tokenized_card_instance.to_dict()
# create an instance of TokenizedCard from a dict
tokenized_card_from_dict = TokenizedCard.from_dict(tokenized_card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


