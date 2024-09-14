# openapi_client.ReversePaymentApi

All URIs are relative to *https://api.mtn.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_reverse_transaction_history**](ReversePaymentApi.md#get_reverse_transaction_history) | **GET** /reverse-payment/history | Provides the history or list of revese transactions  to third party.


# **get_reverse_transaction_history**
> ReverseTransactionHistory get_reverse_transaction_history(customer_id, transactiontype, correlator_id=correlator_id, transaction_id=transaction_id, transactionstatus=transactionstatus, amount=amount, x_authorization=x_authorization, node_id=node_id, start_date=start_date, end_date=end_date, other_fri=other_fri, pos_msisdn=pos_msisdn, quote_id=quote_id, limit=limit, page_no=page_no)

Provides the history or list of revese transactions  to third party.

Provides the status of a Payment Transaction to service providers.

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.reverse_transaction_history import ReverseTransactionHistory
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
    api_instance = openapi_client.ReversePaymentApi(api_client)
    customer_id = 'FRI:266456789/MSISDN' # str | Unique identifier of the customer. It should be financial resource identification in case of target system is ECW
    transactiontype = 'transactiontype_example' # str | transactiontype
    correlator_id = 'c5f80cb8-dc8b-11ea-87d0-0242ac130003' # str | Unique identifier in the client for the payment in case it is needed to correlate. (optional)
    transaction_id = '6f0bece6-7df3-4da4-af02-5e7f16e5e6fc' # str | Client generated Id to include for tracing requests. (optional)
    transactionstatus = 'transactionstatus_example' # str | This is the provider that is expected to fulfill the query transaction service (optional)
    amount = 3.4 # float | amount of the transaction (optional)
    x_authorization = 'x_authorization_example' # str | Encrypted ECW credentials (optional)
    node_id = 'node_id_example' # str | Third parties unique identifier. Can also be called channelId. (optional)
    start_date = 'start_date_example' # str | Retrieve transaction history created  from this start date. (optional)
    end_date = 'end_date_example' # str | Retrieve transaction history created until this stop date. (optional)
    other_fri = 'other_fri_example' # str | The FRI of the other party in transaction, could be from or to depending on direction. Validated with IsFRI. (optional)
    pos_msisdn = 'pos_msisdn_example' # str | Retrieve transaction history performed be the specified point of sale MSISDN. (optional)
    quote_id = 'quote_id_example' # str | List all information based on quoteId  then quoteId used. (optional)
    limit = 1 # int | The maximum number of items to return in the response. Default value 50. (optional) (default to 1)
    page_no = 56 # int | indexoffset the list of results returned by an API. Optional, If its not specified we should return all the values. (optional)

    try:
        # Provides the history or list of revese transactions  to third party.
        api_response = api_instance.get_reverse_transaction_history(customer_id, transactiontype, correlator_id=correlator_id, transaction_id=transaction_id, transactionstatus=transactionstatus, amount=amount, x_authorization=x_authorization, node_id=node_id, start_date=start_date, end_date=end_date, other_fri=other_fri, pos_msisdn=pos_msisdn, quote_id=quote_id, limit=limit, page_no=page_no)
        print("The response of ReversePaymentApi->get_reverse_transaction_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReversePaymentApi->get_reverse_transaction_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **str**| Unique identifier of the customer. It should be financial resource identification in case of target system is ECW | 
 **transactiontype** | **str**| transactiontype | 
 **correlator_id** | **str**| Unique identifier in the client for the payment in case it is needed to correlate. | [optional] 
 **transaction_id** | **str**| Client generated Id to include for tracing requests. | [optional] 
 **transactionstatus** | **str**| This is the provider that is expected to fulfill the query transaction service | [optional] 
 **amount** | **float**| amount of the transaction | [optional] 
 **x_authorization** | **str**| Encrypted ECW credentials | [optional] 
 **node_id** | **str**| Third parties unique identifier. Can also be called channelId. | [optional] 
 **start_date** | **str**| Retrieve transaction history created  from this start date. | [optional] 
 **end_date** | **str**| Retrieve transaction history created until this stop date. | [optional] 
 **other_fri** | **str**| The FRI of the other party in transaction, could be from or to depending on direction. Validated with IsFRI. | [optional] 
 **pos_msisdn** | **str**| Retrieve transaction history performed be the specified point of sale MSISDN. | [optional] 
 **quote_id** | **str**| List all information based on quoteId  then quoteId used. | [optional] 
 **limit** | **int**| The maximum number of items to return in the response. Default value 50. | [optional] [default to 1]
 **page_no** | **int**| indexoffset the list of results returned by an API. Optional, If its not specified we should return all the values. | [optional] 

### Return type

[**ReverseTransactionHistory**](ReverseTransactionHistory.md)

### Authorization

[OAuth2](../README.md#OAuth2)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, The services object/envelope will be null

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

