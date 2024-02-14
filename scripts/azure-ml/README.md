# Creating and using an Azure ML model endpoint

This folder contains code and instructions for creating and using an [Azure Machine Learning (Azure ML)](https://azure.microsoft.com/en-us/products/machine-learning) LLM endpoint.

## Creating an Azure ML workspace

To create an Azure ML endpoint, you need to first have an Azure ML workspace:
1. Sign into the Azure portal.
2. Create a resource group within the subscription that you want to use for your workspace and host your endpoint.
3. Create an Azure Machine Learning service workspace.
    - When a workspace is created, Azure will automatically create other resources within the same resource group, such as a storage account, key vault.

Note: There are several ways to create an Azure ML workspace. Either by using the Azure portal as described above, or by using the Azure CLI, or by using the Azure ML Python SDK. 
For using the Azure CLI, we provide an example bash script in [azure_ml_setup_cli.sh](azure_ml_setup_cli.sh). The script takes a subscription name or ID as input and will create a resource group called `"rg-llm-endpoint"` and azure ml workspace called `"llm-endpoint-ml"` in the East US2 region (note: at time of writing, pay-as-you-go model deployment is only available for workspaces created in East US2 and West US3 regions).

For setting up the Azure CLI or Azure SDK, see the following resources:
- [Installing and setting up Azure CLI](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?view=azureml-api-2&tabs=public)
- [Installing and setting up Azure SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-ml-readme?view=azure-python)

Notes:
- To create an Azure ML workspace and for general grant access to operations in Azure ML, you need to have the appropriate permissions. Generally, for most tasks, your user account must be assigned the "owner" or "contributor" role for the Azure subscription. For more specific actions, you may need more granular permissions.
- Whenever using the Azure CLI, you must set the account to the right subscription with `az account set --name "your-subscription-name-or-id"`.
    - You can use `azure account list` to list all subscriptions and `az account show` to show the current subscription.

## Creating Azure ML endpoint

There are two types of endpoints in Azure ML: [realtime](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints-online?view=azureml-api-2) (which can also be pay-as-you-go in some cases) and [batch](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints-batch?view=azureml-api-2). Here, we just cover setting up a realtime endpoint or a pay-as-you-go endpoint.

Once you have an Azure ML workspace, you can create a model endpoint via the Azure ML studio and select your workspace that you want to work in. 
1. Select the model you want to deploy from the [model catalog](https://ml.azure.com/model/catalog) - see [here](https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-catalog?view=azureml-api-2) for an overview of the model catalog.
2. Click "Deploy" and select "Realtime endpoint" (or "pay-as-you-go" endpoint, if available for the model you want to deploy).
3. Fill in the required information, such as the name of the endpoint, the compute type, and the deployment configuration.

Note that you may not have the quota required in order to deploy a model. However, for Azure ML, you can use the option to use a [**shared quota**](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-quotas?view=azureml-api-2#azure-machine-learning-shared-quota) which allows you to deploy an endpoint for a limited time. This is useful for testing and development purposes but Azure does not recommend this for production use. You can also request for quota for permanent deployment of an endpoint.

For more general information on deploying model endpoints in Azure ML:
- [Deploying Llama2 family model endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-models-llama?view=azureml-api-2)
- [Deploy and score a machine learning model by using an online endpoint](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-online-endpoints?view=azureml-api-2&tabs=azure-cli)
- [Batch endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints-batch?view=azureml-api-2)

## Querying your Azure ML endpoint

Once you have deployed an endpoint, you can query the model by sending a request to the endpoint. The model that you deployed from the model catalog will typically include details of the input and output formats for the model. There are different ways to send a request to the endpoint, such as using the Azure CLI (via the `az ml model invoke` command), using the Azure ML SDK, or using a REST API call. 

The process for querying a realtime endpoint or a pay-as-you-go endpoint is largely the same besides your request input may be different. In particular, see some examples in this folder:
- [llama2_request.json](llama2_request.json) and [llama_2_request_2.json](llama_2_request_2.json) are example input JSON requests for querying a PAYG Llama2 model endpoint.
- [realtime_request.json](realtime_request.json) is an example input JSON request for querying a realtime endpoint for Llama2 model.
    - Other open source models on Azure ML such as Mistral's models also use this same format.
    - Generally, just see the model page on the model catalog for the input format for the model you want to query.

Note: For a PAYG endpoint, it seems like you can only query the endpoint using a REST API call. Using the below instructions for querying via the Azure CLI or Azure ML SDK does not seem to work for PAYG endpoints. Please let us know if you have any success with this.

### Using the Azure CLI

You can use the [`az ml online-endpoint invoke`](https://learn.microsoft.com/en-us/cli/azure/ml/online-endpoint?view=azure-cli-latest#az-ml-online-endpoint-invoke) command to send a request to the endpoint, e.g.
```bash
az ml online-endpoint invoke --name ENDPOINT_NAME --request-file input-json.json --resource-group RESOURCE_GROUP --workspace-name WORKSPACE_NAME
```

### Using the Azure ML SDK

It is also possible to use the Azure ML SDK to send a request to the endpoint, e.g.

```python
from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)

# set up credentials for request (i.e. login to Azure account)
try:
    credential = DefaultAzureCredential()
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    credential = InteractiveBrowserCredential()

# set up variables for request
SUBSCRIPTION_ID = "your-subscription-id"
RESOURCE_GROUP_NAME = "your-resource-group-name"
WORKSPACE_NAME = "your-workspace-name"
ENDPOINT_NAME = "your-endpoint-name"
input_json = "your-input-json-file.json"

workspace_ml_client = MLClient(
    credential,
    subscription_id=SUBSCRIPTION_ID,
    resource_group_name=RESOURCE_GROUP_NAME,
    workspace_name=WORKSPACE_NAME,
)

response = workspace_ml_client.online_endpoints.invoke(
    endpoint_name=ENDPOINT_NAME,
    request_file=input_json,
)
```

We provide an example Python script for querying an endpoint using the Azure ML SDK in [request_to_endpoint_azure_ml.py](request_to_endpoint_azure_ml.py) where you can just pass in the input JSON file as an argument.
```bash
python request_to_endpoint_azure_ml.py --input-json realtime_request.json
```

### Using a REST API call

You can also use a REST API call to send a request to the endpoint. The endpoint URL and the input JSON format will be provided in the model catalog for the model you want to query.
```rest
Host: <DEPLOYMENT_URI>
Authorization: Bearer <TOKEN>
Content-type: application/json
```

In Python, you can simply use the `requests` library to send a request to the endpoint, e.g.
```python
import requests
import json

# set up variables for request
API_URL = "your-endpoint-url"
ENDPOINT_TOKEN = "your-endpoint-token"
headers = {"Authorization":f"Bearer {ENDPOINT_TOKEN}", "Content-Type":"application/json"}

response = requests.post(API_URL, data=data, headers=headers)
```
where `data` is the string of your request input JSON.

We provide an example Python script for querying an endpoint using a REST API call in [request_to_endpoint.py](request_to_endpoint.py) where you can just pass in the input JSON file as an argument, and you must set the `API_URL` and `ENDPOINT_TOKEN` environment variables.
```bash
export API_URL="your-endpoint-url"
export ENDPONT_TOKEN="your-endpoint-token"
python request_to_endpoint.py --input-json realtime_request.json
```

Note:
- For completions models, such as Llama-2-7b, use the `<target_url>/v1/completions` API.
- For chat models, such as Llama-2-7b-chat, use the `<target_url>/v1/chat/completions` API.
