from transformers import AutoTokenizer


def get_n_tokens(text: str, model_name: str) -> int:
    """
    Function to get the number of tokens in a given text using a specified model.

    Parameters:
    text (str): The text to tokenize.
    model_name (str): The name of the model to use for tokenization.

    Returns:
    int: The number of tokens in the text.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return len(tokenizer.encode(text))


def get_cost_estimate(
    len_input: int,
    max_len_output: int,
    cost_input_token: float,
    cost_output_token: float,
) -> float:
    """
    Function to estimate the cost of tokenization.

    Parameters:
    len_input (int): The number of input tokens.
    max_len_output (int): The max number of output tokens.
    cost_input_token (float): The cost per input token.
    cost_output_token (float): The cost per output token.

    Returns:
    float: The estimated cost of tokenization.
    """
    return len_input * cost_input_token + max_len_output * cost_output_token


if __name__ == "__main__":

    # Cost per input token in USD
    cost_input_token = 0.00000081

    # Cost per output token in USD
    cost_output_token = 0.00000094

    # Input prompt
    input_prompt = "The quick brown fox jumps over the lazy dog."

    # Max length of output
    max_len_output = 2048

    # Model name
    model_name = "meta-llama/Llama-2-7b-chat-hf"

    # Get the number of tokens in the input prompt
    len_input = get_n_tokens(input_prompt, model_name)

    # Estimate the PAYG cost
    cost_estimate = get_cost_estimate(
        len_input, max_len_output, cost_input_token, cost_output_token
    )
    print(f"Estimated PAYG cost: ${cost_estimate}")
