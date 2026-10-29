"""Task 2.4: Batch Product Writer.

Writes a one-sentence menu description for every product in one run and
reports the total tokens and time. Products with no price are skipped,
so no AI money is spent on them.
"""

from langchain.chat_models import init_chat_model

# A price of 0 means old stock that we do not sell any more.
products = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
    "donut": 200,
    "old stock": 0,
}

# The model is created ONCE, before the loop. Creating it inside the loop
# would reload it for every product and waste time.
llm = init_chat_model("gemma4:31b-cloud", model_provider="ollama", temperature=0.2)

# Accumulators start at 0 BEFORE the loop, or they would reset every round.
total_tokens = 0
total_seconds = 0
results = []

for name, price in products.items():
    # continue jumps to the next product, so no AI call (and no tokens) is spent.
    if price == 0:
        print(f"Skipping {name} (no price)")
        continue

    response = llm.invoke(f"Write one short, tasty sentence for a bakery menu describing a {name}. Reply with the sentence only.")

    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

    # A list of dictionaries keeps item, price and text together.
    results.append({"item": name, "price": price, "text": response.text.strip()})

print("=" * 50)
for number, entry in enumerate(results, start=1):
    print(f"{number}. {entry['item'].title()} ({entry['price']} PKR)")
    print(f"   {entry['text']}")
print("=" * 50)
print(f"{len(results)} descriptions, {total_tokens} tokens, {total_seconds:.1f} seconds")