# Overview

This is a collection of various scripts LLM related.

## LLM API setup

To set up an LLM endpoint, you can use the `setup_llm_endpoint.py` script. The LLM API is a simple FastAPI app that can be run on a machine to host a model. The script sets up a Huggingface `transformers` text-generation pipeline which you will be able to query. For example, to set up a Llama2 endpoint, you can run:
```bash
# export HF token since you need to have been granted access to the model
export HUGGINGFACE_TOKEN=YOUR_HUGGINGFACE_TOKEN
# set up the endpoint
python setup_llm_endpoint.py --model meta-llama/Llama-2-13b-chat
```

Note this by default sets the host to `0.0.0.0` and port to `8000`. You can change these by passing in the `--host` and `--port` arguments in the CLI. You might want to set the host to be something local if you want to host it on the same machine you're running on:
```bash
python src/setup_llm_endpoint.py --model microsoft/phi-1_5 --host 127.0.0.1
```

And should be able to query it on the same machine via cURL the following way:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"prompt": "This is a test prompt"}' \
  http://127.0.0.1:8000/predict
```

And via Python the following way:

```python
import requests

url = 'http://127.0.0.1:8000/predict'
data = {
    "prompt": "This is a test prompt"
}

response = requests.post(url, json=data)
print(response.json())
```
