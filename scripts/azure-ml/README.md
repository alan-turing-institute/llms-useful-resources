**README IN WIP**

## Usage:
- Set API_URL and ENDPOINT_TOKEN environment variables
- For a realtime endpoint and a PAYG endpoint, can use `request_to_endpoint.py` to send a request to the endpoint, e.g. 
```
python request_to_endpoint.py --input-json realtime_request.json
```
and 
```
python request_to_endpoint.py --input-json llama2_request.json
```
- For a realtime endpoint, alternatively, you can use the Azure ML SDK to invoke the endpoint, e.g.
```
python request_to_endpoint_azure_ml.py --input-json realtime_request.json
```
Currenlty, it seems you cannot do this for a PAYG endpoint as it's not able to be accessed via the Azure ML SDK.

## Some links to add:
- [Installing and setting up Azure CLI](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?view=azureml-api-2&tabs=public)
- [Deploying Llama2 models](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-models-llama?view=azureml-api-2)
- [Azure ML model catalog](https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-catalog?view=azureml-api-2)

## TODO:
- Python environment setup instructions
- How to deploy a model in Azure ML
- Links to endpoint documentation (explain input json format, expected output format, etc.)