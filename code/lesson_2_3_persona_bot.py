"""Task 2.3: Persona Bot with Real Facts.

An AI assistant for Sweet Crumbs bakery (change the facts for your own
business). It may ONLY use the facts we give it, so it cannot invent prices.
Commands: /persona <name>, /price <item>, /add <item> <price>, bye.
"""

from langchain.chat_models import init_chat_model

# Real facts about the business. The AI is told to use only these.
facts = {
    "name": "Sweet Crumbs bakery",
    "type": "bakery",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "delivery": "200 PKR, free from 3,000 PKR",
    "prices": {"cupcake": 250, "brownie": 300, "chocolate cake": 1500},
}

personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, short precise sentences",
    "sales": "excited, always suggests one extra item to buy",
}

# One config dictionary, so changing the model, temperature or memory
# size means editing one line instead of searching the whole file.
config = {"model": "gemma4:31b-cloud", "temperature": 0.2, "memory_size": 8}

llm = init_chat_model(config["model"], model_provider="ollama", temperature=config["temperature"])

# The system message is built from the facts with f-strings. "Only use
# these facts" is the safety rule that stops the AI inventing prices.
base_rules = f"""You are the assistant of {facts['name']}, a {facts['type']} in {facts['city']}.
Only use these facts. Hours: {facts['hours']}. Delivery: {facts['delivery']}.
If something is not in these facts, say you do not know. Never invent prices or promises.
Answer in 2 short lines. """
prices_line = f"Prices in PKR: {facts['prices']}. "
current_style = personas["friendly"]

messages = [{"role": "system", "content": base_rules + prices_line + f"Style: {current_style}"}]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, bye")

while True:
    user_text = input("You: ").strip()
    command = user_text.lower()

    if command == "bye":
        print("Bot: Goodbye!")
        break
    elif command.startswith("/persona"):
        style_name = command[8:].strip()
        # .get() with a default means a wrong name (like "pirate") falls
        # back to friendly instead of crashing with a KeyError.
        current_style = personas.get(style_name, personas["friendly"])
        messages[0]["content"] = base_rules + prices_line + f"Style: {current_style}"
        print(f"Bot: Style changed to: {current_style}")
    elif command.startswith("/price"):
        item = command[6:].strip()
        # Prices come straight from the dictionary, NOT from the AI, so the
        # answer is always exact. 0 means "not on our menu".
        price = facts["prices"].get(item, 0)
        if item == "":
            print("Bot: Please type an item, like /price cupcake")
        elif price == 0:
            print(f"Bot: Sorry, {item} is not on our menu.")
        else:
            print(f"Bot: {item.capitalize()} costs {price:,} PKR.")
    elif command.startswith("/add"):
        # Stretch: /add <item> <price> adds to the dictionary AND rebuilds
        # the system message, so the AI knows the new item immediately.
        rest = command[4:].strip()
        if " " in rest and rest.rsplit(" ", 1)[1].isdigit():
            item_text, price_text = rest.rsplit(" ", 1)
            facts["prices"][item_text.strip()] = int(price_text)
            prices_line = f"Prices in PKR: {facts['prices']}. "
            messages[0]["content"] = base_rules + prices_line + f"Style: {current_style}"
            print(f"Bot: Added {item_text.strip()} at {int(price_text):,} PKR.")
        else:
            print("Bot: Use /add <item> <price>, like /add donut 200")
    elif user_text == "":
        print("Bot: Please type a question.")
    else:
        messages.append({"role": "user", "content": user_text})
        # Memory trimming from Task 2.2, using the size from config.
        messages = [messages[0]] + messages[1:][-config["memory_size"]:]
        response = llm.invoke(messages)
        messages.append({"role": "assistant", "content": response.text})
        print(f"Bot: {response.text}")