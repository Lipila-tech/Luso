# openapi_client.PaymentHistoryApi

All URIs are relative to *https://api.mtn.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_payment_history**](PaymentHistoryApi.md#get_payment_history) | **GET** /payments/{id}/history | Get a list of payments made on a reference or by a customer id


# **get_payment_history**
> PaymentHistoryResponse get_payment_history(id, x_authorization=x_authorization, transaction_id=transaction_id, target_system=target_system, segment=segment, id_type=id_type, page_size=page_size, page_number=page_number, status=status, request_type=request_type, node_id=node_id, start_time=start_time, start_date=start_date, end_date=end_date, query_type=query_type, registration_channel=registration_channel, trace_id=trace_id)

Get a list of payments made on a reference or by a customer id

Get a list of payments made on a reference or by a customer id

### Example

* OAuth Authentication (OAuth2):

```python
import openapi_client
from openapi_client.models.payment_history_response import PaymentHistoryResponse
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
    api_instance = openapi_client.PaymentHistoryApi(api_client)
    id = 'c5f80cb8-dc8b-11ea-87d0-0242ac130003' # str | Unique identifier in the client for the payment in case it is needed to correlate.
    x_authorization = 'x_authorization_example' # str | An authorization claim to be passed by the caller (optional)
    transaction_id = '6f0bece6-7df3-4da4-af02-5e7f16e5e6fc' # str | Client generated Id to include for tracing requests. (optional)
    target_system = 'target_system_example' # str | target system expected to fulful the service (optional)
    segment = 'segment_example' # str | Segment of the customer. For example, subscriber,agent, merchant, admin depending on the type of customer whome the operation is being performed against. (optional)
    id_type = 'id_type_example' # str | Type of the customerId in the path. (optional)
    page_size = 10 # float | Maximum number of items to get from the backend system (optional)
    page_number = 0 # float | Current page or offset number (optional)
    status = 'SUCCESSFUL' # str | Status of the transactions (optional)
    request_type = 'request_type_example' # str | type of request (optional)
    node_id = 'Comviva' # str | Node making the request (optional)
    start_time = '20210622131709' # str | Start time of the transaction.If blank, then transaction received date will be set as start time (optional)
    start_date = '20210622131709' # str | Start date of the history range (optional)
    end_date = '20220629120000' # str | End date of the history range (optional)
    query_type = 'Y' # str | Type of request (optional)
    registration_channel = 'SMS' # str | Channel making the request (optional)
    trace_id = '156135egfSfgfgadg09676' # str | Unique identifier from the caller (optional)

    try:
        # Get a list of payments made on a reference or by a customer id
        api_response = api_instance.get_payment_history(id, x_authorization=x_authorization, transaction_id=transaction_id, target_system=target_system, segment=segment, id_type=id_type, page_size=page_size, page_number=page_number, status=status, request_type=request_type, node_id=node_id, start_time=start_time, start_date=start_date, end_date=end_date, query_type=query_type, registration_channel=registration_channel, trace_id=trace_id)
        print("The response of PaymentHistoryApi->get_payment_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PaymentHistoryApi->get_payment_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier in the client for the payment in case it is needed to correlate. | 
 **x_authorization** | **str**| An authorization claim to be passed by the caller | [optional] 
 **transaction_id** | **str**| Client generated Id to include for tracing requests. | [optional] 
 **target_system** | **str**| target system expected to fulful the service | [optional] 
 **segment** | **str**| Segment of the customer. For example, subscriber,agent, merchant, admin depending on the type of customer whome the operation is being performed against. | [optional] 
 **id_type** | **str**| Type of the customerId in the path. | [optional] 
 **page_size** | **float**| Maximum number of items to get from the backend system | [optional] 
 **page_number** | **float**| Current page or offset number | [optional] 
 **status** | **str**| Status of the transactions | [optional] 
 **request_type** | **str**| type of request | [optional] 
 **node_id** | **str**| Node making the request | [optional] 
 **start_time** | **str**| Start time of the transaction.If blank, then transaction received date will be set as start time | [optional] 
 **start_date** | **str**| Start date of the history range | [optional] 
 **end_date** | **str**| End date of the history range | [optional] 
 **query_type** | **str**| Type of request | [optional] 
 **registration_channel** | **str**| Channel making the request | [optional] 
 **trace_id** | **str**| Unique identifier from the caller | [optional] 

### Return type

[**PaymentHistoryResponse**](PaymentHistoryResponse.md)

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

