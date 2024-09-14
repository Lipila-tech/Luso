# openapi_client.P2pTransferFeeCheckApi

All URIs are relative to *https://api.mtn.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**inbound**](P2pTransferFeeCheckApi.md#inbound) | **POST** /payments/fee | check transfer fee/charges beforhand


# **inbound**
> InboundResponse inbound(body)

check transfer fee/charges beforhand

Provides the ability for a consumer to check a payment transfer fee charged by service providers.

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.feecheck_request import FeecheckRequest
from openapi_client.models.inbound_response import InboundResponse
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
    api_instance = openapi_client.P2pTransferFeeCheckApi(api_client)
    body = openapi_client.FeecheckRequest() # FeecheckRequest | request body

    try:
        # check transfer fee/charges beforhand
        api_response = api_instance.inbound(body)
        print("The response of P2pTransferFeeCheckApi->inbound:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling P2pTransferFeeCheckApi->inbound: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeecheckRequest**](FeecheckRequest.md)| request body | 

### Return type

[**InboundResponse**](InboundResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad Request |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

