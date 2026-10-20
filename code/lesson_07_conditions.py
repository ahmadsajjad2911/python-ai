"""Task 1.7: Smart Model Router.

Chooses a model by task type (code, private or chat) and estimates the
cost, so private data stays local and cheap tasks use a cheap model.
"""

# strip().lower() lets " Code " and "CODE" both work.
task_type = input("Task (code / private / chat): ").strip().lower()
tokens = int(input("Estimated tokens: "))

# Paid users may send long requests (stretch)
is_paid = input("Is this a paid user? (yes/no): ").strip().lower()

# Each task gets its own model and example price per 1K tokens.
if task_type == "code":
    model = "claude (cloud, strong at code)"
    price = 0.8
elif task_type == "private":
    # Private data must never leave the machine, so we use a local model.
    model = "llama3.2 (local, Ollama)"
    price = 0
elif task_type == "chat":
    model = "haiku (cloud, cheap)"
    price = 0.1
else:
    model = "none (unknown task type)"
    price = 0

# Long requests cost more, so we warn before the money is spent.
if tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

# Stretch: free users with long requests are asked to upgrade
if is_paid == "no" and tokens > 2000:
    print("Upgrade to send long requests.")

cost = tokens / 1000 * price
print(f"Chosen model: {model}")
print(f"Estimated cost: {cost:.2f} PKR")