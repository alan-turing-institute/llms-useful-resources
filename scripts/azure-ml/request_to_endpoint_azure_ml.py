from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoke a realtime endpoint")
    parser.add_argument('--input-json', type=str, help='input json file', default="realtime_request.json")
    parser.add_argument("--subscription-id", type=str, help="The subscription name/id")
    parser.add_argument("--endpoint", type=str, help="The name of the endpoint to invoke")
    args = parser.parse_args()
    
    print("Signing in to Azure...")
    
    try:
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
    except Exception as ex:
        credential = InteractiveBrowserCredential()

    RESOURCE_GROUP_NAME="rg-llm-endpoint"
    WORKSPACE_NAME="llm-endpoint-ml"

    workspace_ml_client = MLClient(
        credential,
        subscription_id=args.subscription_id,
        resource_group_name=RESOURCE_GROUP_NAME,
        workspace_name=WORKSPACE_NAME,
    )
    
    print("Invoking endpoint...")

    response = workspace_ml_client.online_endpoints.invoke(
        endpoint_name=args.endpoint,
        request_file=args.input_json,
    )
    
    print("raw response: \n", response, "\n")