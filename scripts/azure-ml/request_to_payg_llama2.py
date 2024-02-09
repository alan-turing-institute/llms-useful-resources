import os
import requests
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Request to Llama-2')
    parser.add_argument('--input-json', type=str, help='input json file', default="llama2_request.json")
    parser.add_argument('--completion', action='store_true', help='use completion mode', default=False)
    
    args = parser.parse_args()
    
    ENDPOINT_TOKEN=os.environ.get("ENDPOINT_TOKEN")
    if not ENDPOINT_TOKEN:
        raise Exception("ENDPOINT_TOKEN environment variable not set")

    API_URL=os.environ.get("API_URL")
    if not API_URL:
        raise Exception("API_URL environment variable not set")

    if args.completion:
        api_url = f"{API_URL}/v1/completions"
    else:
        api_url = f"{API_URL}/v1/chat/completions"

    headers =  {"Authorization":f"Bearer {ENDPOINT_TOKEN}", "Content-Type":"application/json"}

    with open(args.input_json) as f:
        request_json = json.dumps(json.load(f))
    
    print(f"Sending request to with data {request_json}\n")
    
    response = requests.post(api_url, data=request_json, headers=headers)

    print(f"response.json():\n{response.json()}\n")
    print(f"output:\n{response.json()['choices'][0]['message']['content']}\n")
    