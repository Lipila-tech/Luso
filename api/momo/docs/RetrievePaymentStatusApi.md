# openapi_client.RetrievePaymentStatusApi

All URIs are relative to *https://api.mtn.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_payment_transaction_status**](RetrievePaymentStatusApi.md#get_payment_transaction_status) | **GET** /payments/{correlatorId}/transactionStatus | Provides the status of a Payment Transaction to service providers.


# **get_payment_transaction_status**
> PaymentTransactionStatusResponse get_payment_transaction_status(correlator_id, transaction_id=transaction_id, x_authorization=x_authorization, amount=amount, target_system=target_system, payment_type=payment_type, customer_id=customer_id, description=description)

Provides the status of a Payment Transaction to service providers.

Provides the status of a Payment Transaction to service providers.

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.payment_transaction_status_response import PaymentTransactionStatusResponse
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
    api_instance = openapi_client.RetrievePaymentStatusApi(api_client)
    correlator_id = 'c5f80cb8-dc8b-11ea-87d0-0242ac130003' # str | Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request
    transaction_id = '6f0bece6-7df3-4da4-af02-5e7f16e5e6fc' # str | Client generated Id to include for tracing requests. (optional)
    x_authorization = 'x_authorization_example' # str | Encrypted ECW credentials (optional)
    amount = 3.4 # float |  (optional)
    target_system = 'target_system_example' # str | target system expected to fulful the service (optional)
    payment_type = 'payment_type_example' # str | Type of the transaction (optional)
    customer_id = 'customer_id_example' # str | This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN (optional)
    description = 'description_example' # str | can be a payer note, a merchant identifier ie. merchantId etc. (optional)

    try:
        # Provides the status of a Payment Transaction to service providers.
        api_response = api_instance.get_payment_transaction_status(correlator_id, transaction_id=transaction_id, x_authorization=x_authorization, amount=amount, target_system=target_system, payment_type=payment_type, customer_id=customer_id, description=description)
        print("The response of RetrievePaymentStatusApi->get_payment_transaction_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RetrievePaymentStatusApi->get_payment_transaction_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **correlator_id** | **str**| Unique identifier in the client for the payment in case it is needed to correlate, could also be a reference id generated when making the request | 
 **transaction_id** | **str**| Client generated Id to include for tracing requests. | [optional] 
 **x_authorization** | **str**| Encrypted ECW credentials | [optional] 
 **amount** | **float**|  | [optional] 
 **target_system** | **str**| target system expected to fulful the service | [optional] 
 **payment_type** | **str**| Type of the transaction | [optional] 
 **customer_id** | **str**| This is the payer mobile number ie. MSISDN. Could be ID:122330399/MSISDN | [optional] 
 **description** | **str**| can be a payer note, a merchant identifier ie. merchantId etc. | [optional] 

### Return type

[**PaymentTransactionStatusResponse**](PaymentTransactionStatusResponse.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Customer not found |  -  |
**405** | Method Not allowed |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

