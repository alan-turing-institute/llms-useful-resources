import argparse
import logging
import os

import transformers
import uvicorn
from fastapi import FastAPI


def main():
    parser = argparse.ArgumentParser(description="Set up LLM endpoint")
    parser.add_argument(
        "--model-name", "-m", help="model name", type=str, required=True
    )
    parser.add_argument("--host", help="host to run on", type=str, default="0.0.0.0")
    parser.add_argument("--port", help="port to run on", type=int, default=8000)
    parser.add_argument(
        "--pipeline-task",
        "-t",
        help="task defining the HF pipeline",
        type=str,
        default="text-generation",
    )

    args = parser.parse_args()

    # initialise logging
    logging.basicConfig(
        datefmt=r"%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)8s] %(message)s",
        level=logging.INFO,
    )

    # set up HuggingFace pipeline for text generation
    try:
        pipeline = transformers.pipeline(
            task=args.pipeline_task,
            model=args.model_name,
            device_map="auto",
            token=os.environ.get("HUGGINGFACE_TOKEN"),
            return_full_text=False,
        )
    except OSError as err:
        raise OSError(
            "Might need to set your HUGGINGFACE_TOKEN environment variable"
        ) from err

    # set up FastAPI
    app = FastAPI()

    # set up basic endpoint for checking if the API is running
    @app.get("/")
    async def root():
        return "Hello World!"

    # set up basic endpoint for obtaining text responses
    @app.get("/generate")
    async def generate_text(prompt: str | list[str]) -> str:
        logging.info(f"Received prompt: {prompt}")
        return pipeline(prompt, num_return_sequences=1)[0]["generated_text"]

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
