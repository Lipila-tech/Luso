# openapi_client.GenerateAPaymentAgreementApi

All URIs are relative to *https://api.mtn.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_payment_agreement**](GenerateAPaymentAgreementApi.md#generate_payment_agreement) | **POST** /payments/payment-agreement | Provides the ability for a consumer to generate a payment agreement (Promise to Pay)
[**get_payment_agreement_eligibility**](GenerateAPaymentAgreementApi.md#get_payment_agreement_eligibility) | **GET** /payments/payment-agreement/eligibility | Provides the ability for a consumer to check the eligibility status for payment agreement


# **generate_payment_agreement**
> PromiseToPayResponse generate_payment_agreement(promise_to_pay_request, transaction_id=transaction_id)

Provides the ability for a consumer to generate a payment agreement (Promise to Pay)

Provides the ability for a consumer to generate a payment agreement (Promise to Pay) so as to enable the customer to make payment to the service providers.

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.promise_to_pay_request import PromiseToPayRequest
from openapi_client.models.promise_to_pay_response import PromiseToPayResponse
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
    api_instance = openapi_client.GenerateAPaymentAgreementApi(api_client)
    promise_to_pay_request = openapi_client.PromiseToPayRequest() # PromiseToPayRequest | Agreement details for the payment promise that is to be created.
    transaction_id = '6f0bece6-7df3-4da4-af02-5e7f16e5e6fc' # str | Client generated Id to include for tracing requests. (optional)

    try:
        # Provides the ability for a consumer to generate a payment agreement (Promise to Pay)
        api_response = api_instance.generate_payment_agreement(promise_to_pay_request, transaction_id=transaction_id)
        print("The response of GenerateAPaymentAgreementApi->generate_payment_agreement:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerateAPaymentAgreementApi->generate_payment_agreement: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promise_to_pay_request** | [**PromiseToPayRequest**](PromiseToPayRequest.md)| Agreement details for the payment promise that is to be created. | 
 **transaction_id** | **str**| Client generated Id to include for tracing requests. | [optional] 

### Return type

[**PromiseToPayResponse**](PromiseToPayResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Success |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Customer not found |  -  |
**405** | Method Not allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_payment_agreement_eligibility**
> PromiseToPayEligibilityResponse get_payment_agreement_eligibility(billing_account_number, transaction_id=transaction_id)

Provides the ability for a consumer to check the eligibility status for payment agreement

Provides the ability for a consumer to check the eligibility status for payment agreement so as to enable the customer to make payment to the service providers.

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.promise_to_pay_eligibility_response import PromiseToPayEligibilityResponse
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
    api_instance = openapi_client.GenerateAPaymentAgreementApi(api_client)
    billing_account_number = 'billing_account_number_example' # str | Singleview billing account number.
    transaction_id = '6f0bece6-7df3-4da4-af02-5e7f16e5e6fc' # str | Client generated Id to include for tracing requests. (optional)

    try:
        # Provides the ability for a consumer to check the eligibility status for payment agreement
        api_response = api_instance.get_payment_agreement_eligibility(billing_account_number, transaction_id=transaction_id)
        print("The response of GenerateAPaymentAgreementApi->get_payment_agreement_eligibility:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerateAPaymentAgreementApi->get_payment_agreement_eligibility: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **billing_account_number** | **str**| Singleview billing account number. | 
 **transaction_id** | **str**| Client generated Id to include for tracing requests. | [optional] 

### Return type

[**PromiseToPayEligibilityResponse**](PromiseToPayEligibilityResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Success |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Customer not found |  -  |
**405** | Method Not allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

