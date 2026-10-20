"""Module 1 Project: AI Front Desk for a Local Business.

Built for Sweet Crumbs bakery (change the constants for your own business).
The bot answers common questions with free rules, gives exact price quotes
with /quote (discount + delivery), and turns every question it cannot answer
into a clean, cost-checked AI prompt. It ends with a session report.
"""

# Constants in UPPER_CASE: values that never change while the program runs.
# Changing the business later means editing only these lines.
BUSINESS_NAME = "Sweet Crumbs bakery"
BOT_NAME = "Sweet Crumbs Desk"
DELIVERY_FEE = 200            # PKR
FREE_DELIVERY_LIMIT = 3000    # PKR, free delivery from this amount
CLOUD_PRICE_PER_1K = 0.1      # PKR, EXAMPLE price per 1K tokens
BULK_MIN_QTY = 10             # items needed for the bulk discount
BULK_DISCOUNT_RATE = 0.10     # 10% off

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

# The name is asked ONCE, before the loop, so we never ask it again
# on every message.
name = input(f"{BOT_NAME}: What is your name? ").strip().title()

# Counters for the session report
message_count = 0
rules_count = 0
unanswered_count = 0
quote_count = 0
quoted_value = 0
complaint_count = 0
total_ai_cost = 0

while True:
    # strip().lower() makes "WHAT are your HOURS" and "  hours " match the same rule.
    message = input(f"{name}: ").strip().lower()

    # Empty input is not a real message, so it is not counted.
    if message != "":
        message_count += 1

    # Human handover and complaints come FIRST, so an unhappy customer
    # always reaches a human and never gets a normal reply like a price.
    # " late" has a space before it (and we add one at the start) so that
    # "chocolate" does not wrongly count as a complaint.
    if "human" in message or "agent" in message:
        print(f"{BOT_NAME}: Connecting you to a human...")
        rules_count += 1
        break
    elif "refund" in message or "complaint" in message or " late" in " " + message:
        complaint_count += 1
        rules_count += 1
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")
    elif message == "":
        print(f"{BOT_NAME}: Please type a question, /quote or bye.")
    elif message == "bye":
        rules_count += 1
        print(f"{BOT_NAME}: Goodbye, {name}!")
        break
    # Short words like "hi" use == / startswith, NOT "in", because
    # "hi" in "which cake is best?" is True and would wrongly greet the user.
    elif message == "hi" or message == "hello" or message.startswith("hi ") or message.startswith("hello") or message.startswith("hey"):
        rules_count += 1
        print(f"{BOT_NAME}: Hello {name}! Ask about hours, location, delivery or our menu.")
    elif message == "/quote":
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # Each item has its own price. 0 means "not on our menu".
        if item == "cupcake":
            unit_price = 250
        elif item == "brownie":
            unit_price = 300
        elif item == "chocolate cake":
            unit_price = 1500
        else:
            unit_price = 0

        # isdigit() checks BEFORE int(), so letters like "abc" never crash the bot.
        if unit_price == 0:
            print(f"{BOT_NAME}: Sorry, {item} is not on our menu.")
        elif not quantity_text.isdigit():
            print(f"{BOT_NAME}: Please type the quantity as a whole number, like 5.")
        elif int(quantity_text) == 0:
            print(f"{BOT_NAME}: The quantity must be at least 1.")
        else:
            quantity = int(quantity_text)
            subtotal = unit_price * quantity

            if quantity >= BULK_MIN_QTY:
                discount = round(subtotal * BULK_DISCOUNT_RATE)
            else:
                discount = 0

            # Delivery is decided AFTER the discount, because the customer
            # really pays the discounted amount. 12 cupcakes = 2,700 PKR,
            # which is below the free-delivery limit, so delivery is charged.
            after_discount = subtotal - discount
            if after_discount >= FREE_DELIVERY_LIMIT:
                delivery = 0
            else:
                delivery = DELIVERY_FEE

            total = after_discount + delivery
            quote_count += 1
            quoted_value += total
            print(f"{BOT_NAME}: {quantity} x {item} = {subtotal:,} PKR")
            print(f"     Discount: -{discount:,} PKR | Delivery: {delivery:,} PKR")
            print(f"     Total: {total:,} PKR")
    elif "hours" in message or "open" in message or "timing" in message:
        rules_count += 1
        print(f"{BOT_NAME}: We are open 9 am to 10 pm, every day.")
    elif "where" in message or "location" in message or "your address" in message:
        rules_count += 1
        print(f"{BOT_NAME}: We are at Main Market, Lahore.")
    elif "delivery" in message or "deliver" in message:
        rules_count += 1
        print(f"{BOT_NAME}: Delivery is {DELIVERY_FEE:,} PKR, free from {FREE_DELIVERY_LIMIT:,} PKR.")
    elif "menu" in message or "price" in message or "cost" in message or "how much" in message:
        rules_count += 1
        print(f"{BOT_NAME}: Cupcake 250, brownie 300, chocolate cake 1,500 PKR. Type /quote for an exact price.")
    else:
        # Smart fallback: the rules cannot answer, so we prepare an AI prompt.
        unanswered_count += 1

        # Capitalise and cut to 150 characters so a huge message
        # cannot create an expensive prompt.
        question = message.capitalize()[:150]
        estimated_tokens = round(len(question) / 4)

        # Private details must never leave this computer, so they go to a
        # free local model; everything else goes to a cheap cloud model.
        if "phone" in message or "cnic" in message or "my address" in message:
            model = "llama3.2 (local, private)"
            ai_cost = 0
        else:
            model = "small cloud model (cheap)"
            ai_cost = estimated_tokens / 1000 * CLOUD_PRICE_PER_1K
        total_ai_cost += ai_cost

        prompt = f"""You are the assistant of {BUSINESS_NAME}.
Answer {name} in 2 short lines. Question: {question}"""
        print(f"{BOT_NAME}: Good question! Routed to: {model} (~{estimated_tokens} tokens)")
        print(f"     Prompt: {prompt}")

print("=" * 50)
print("Session report")
print(f"Messages: {message_count} | Answered by rules: {rules_count} | Unanswered: {unanswered_count}")
print(f"Quotes: {quote_count} | Quoted value: {quoted_value:,} PKR")
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print(f"Complaints received: {complaint_count}")
print("=" * 50)