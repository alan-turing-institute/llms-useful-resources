# Build, Quantize, and Run Llama-2-7b Models on Mac using llama.cpp

**Hardware Specs:** Apple M1 Pro - 32GB

The instructions are based on [karankakwani's blog post](https://medium.com/@karankakwani/build-and-run-llama2-llm-locally-a3b393c1570e). The blog post is working fine. Just ensure the model weights and vocab files are downloaded correctly. The only error I got during this process was related to vocab file, which turned out it was corrupted due to a network error.

## Important Note

It is possible to download quantized versions of Llama (and other models) from the Hugging Face hub, eliminating the need for manual quantization. For instance, [The Bloke](https://huggingface.co/TheBloke) account features numerous pre-quantized models. However, it is crucial to consider potential security risks associated with model downloads:

- Models may be susceptible to injection of adversarial behaviors specific to certain prompts.
- Downloaded models can exhibit malicious behavior.

**Possible Mitigations:**

1. You can encapsulate the development environment within containers to enhance isolation and security.
2. Another approach can be executing adversarial datasets to observe and evaluate model behavior. Refer to [HF's Read Teaming Page](https://huggingface.co/blog/red-teaming) for additional insights on analyzing model behavior through this approach.
3. Stay informed about recent and most common AI-model attacks. The [OWASP Top 10](https://owasp.org/www-project-machine-learning-security-top-10/) on Machine Learning Security provides valuable information on current common attack types.

Although these mitigations cannot guarantee full protection, you can minimize the risk and enhance the security posture when working with downloaded quantized models from the Hugging Face hub.

## llama and llama2.cpp Repositories

```dotnetcli
mkdir llm-world
cd llm-world
git clone https://github.com/facebookresearch/llama.git
git clone https://github.com/ggerganov/llama.cpp.git
```

## Download the Models

Follow the steps in the [Llama-2 home page](https://llama.meta.com/).

Note that the model links are only valid for twenty four hours and you can use them to download each model up to five times. After your first request, you can request it multiple times, and it will probably approved instantly by an automatic check.

```dotnetcli
cd llama
chmod 755 ./download.sh
./download.sh
```

## Build llama.cpp

```dotnetcli
cd ../llama.cpp
make
```

## Convert the Model

Create a virtual environment:

```dotnetcli
cd ..
python -m venv llmenv
source llmenv/bin/activate
python3 -m pip install -r ./llama.cpp/requirements.txt
```

Convert the model:

```
mkdir ./llama.cpp/models/7B
python3 convert.py --outfile ./llama.cpp/models/7B/ggml-model-f16.bin --outtype f16 ./llama/llama-2-7b-chat --vocab-dir ./llama
```

## Quantize the Model

```dotnetcli
cd ./llama.cpp
./quantize  ./models/7B/ggml-model-f16.bin ./models/7B/ggml-model-q4_0.bin q4_0
```

## Test the Model on Local

```dotnetcli
./main -m ./models/7B/ggml-model-q4_0.bin -n 1024 --repeat_penalty 1.0 --color -i -r "User:" -f ./prompts/chat-with-bob.txt
```