import os
import requests
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Request to Azure ML endpoint')
    parser.add_argument('--input-json', type=str, help='input json file', default="llama2_request.json")
    
    args = parser.parse_args()
    
    ENDPOINT_TOKEN=os.environ.get("ENDPOINT_TOKEN")
    if not ENDPOINT_TOKEN:
        raise Exception("ENDPOINT_TOKEN environment variable not set")

    API_URL=os.environ.get("API_URL")
    if not API_URL:
        raise Exception("API_URL environment variable not set")

    headers =  {"Authorization":f"Bearer {ENDPOINT_TOKEN}", "Content-Type":"application/json"}

    with open(args.input_json) as f:
        request_json = json.dumps(json.load(f))
    
    print(f"Sending request to with data {request_json}\n")
    
    response = requests.post(API_URL, data=request_json, headers=headers)

    print(f"response.json():\n{response.json()}\n")
    