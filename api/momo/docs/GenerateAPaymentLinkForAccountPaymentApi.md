# openapi_client.GenerateAPaymentLinkForAccountPaymentApi

All URIs are relative to *https://api.mtn.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_payment_link**](GenerateAPaymentLinkForAccountPaymentApi.md#generate_payment_link) | **POST** /payments/payment-link | Provides the ability for a consumer to generate a payment link for account payment


# **generate_payment_link**
> OrderResponse generate_payment_link(order_request, transaction_id=transaction_id)

Provides the ability for a consumer to generate a payment link for account payment

Provides the ability for a consumer to get the payment link for the requesting MSISDN so as to enable the customer to make payment to the service providers.

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.order_request import OrderRequest
from openapi_client.models.order_response import OrderResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.mtn.com/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://api.mtn.com/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.GenerateAPaymentLinkForAccountPaymentApi(api_client)
    order_request = openapi_client.OrderRequest() # OrderRequest | Order details for the payment link that is to be created.
    transaction_id = '6f0bece6-7df3-4da4-af02-5e7f16e5e6fc' # str | Client generated Id to include for tracing requests. (optional)

    try:
        # Provides the ability for a consumer to generate a payment link for account payment
        api_response = api_instance.generate_payment_link(order_request, transaction_id=transaction_id)
        print("The response of GenerateAPaymentLinkForAccountPaymentApi->generate_payment_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerateAPaymentLinkForAccountPaymentApi->generate_payment_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_request** | [**OrderRequest**](OrderRequest.md)| Order details for the payment link that is to be created. | 
 **transaction_id** | **str**| Client generated Id to include for tracing requests. | [optional] 

### Return type

[**OrderResponse**](OrderResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**201** | Success |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Customer not found |  -  |
**405** | Method Not allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

