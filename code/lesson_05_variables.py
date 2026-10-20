"""Task 1.5: AI Model Profile Card.

Stores a model profile using all 4 basic types (str, int, float, bool),
prints each with its type, and estimates the cost of one chat and one month.
"""

# snake_case names, and no built-in names like input or type, so we never
# overwrite Python's own tools by accident.
model_name = "llama3.2"        # str
context_window = 128000        # int (tokens), check ollama.com/library
price_per_1k = 0.5             # float, EXAMPLE price in PKR per 1K tokens
runs_locally = True            # bool

print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window} tokens {type(context_window)}")
print(f"Price per 1K tokens: {price_per_1k} PKR {type(price_per_1k)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# input() returns text, so int() turns it into a number we can calculate with.
tokens_per_chat = int(input("Tokens per chat: "))

# Cost = (tokens / 1000) * price per 1K. round() keeps money to 2 decimals.
estimated_cost = round(tokens_per_chat / 1000 * price_per_1k, 2)

print(f"Tokens per chat: {tokens_per_chat}")
print(f"Estimated cost: {estimated_cost} PKR")

# Stretch: monthly cost for 30 days
chats_per_day = int(input("Chats per day: "))
monthly_cost = round(estimated_cost * chats_per_day * 30, 2)
print(f"Estimated monthly cost (30 days): {monthly_cost} PKR")