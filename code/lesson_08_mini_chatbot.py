"""Task 1.8: Business Helper Bot (Module 1 final).

A rule-based chatbot for a local business. It answers common questions,
hands complaints to a human, counts what it could not answer, and prints
the AI prompt we will send in Module 2.
"""

# Change these two lines to match your real business.
business_name = "City Care Clinic"
bot_name = f"{business_name} Bot"

print(f"{bot_name}: Hi! Ask about timings, fees, location or appointments. Type 'bye' to exit.")

# The name is asked ONCE, before the loop, so we do not ask on every message.
name = input(f"{bot_name}: What is your name? ").strip().title()

message_count = 0
unanswered_count = 0
complaint_count = 0

while True:
    # strip().lower() makes "TIMINGS" and "  timings " match the same rule.
    message = input(f"{name}: ").strip().lower()
    message_count += 1

    # Complaint / handover rules come FIRST so an angry customer is never
    # answered with a normal reply like "our fee is 2,000".
    if "human" in message or "agent" in message:
        print(f"{bot_name}: Connecting you to a human...")
        break
    elif "complaint" in message or "late" in message or "refund" in message or "rude" in message:
        complaint_count += 1
        print(f"{bot_name}: Sorry about that. The clinic manager will call you today.")
    elif message == "bye":
        print(f"{bot_name}: Take care, {name}!")
        break
    # Short words like "hi" use == / startswith, NOT "in", because
    # "hi" in "which" is True and would wrongly trigger a greeting.
    elif message == "hi" or message == "hello" or message.startswith("hey"):
        print(f"{bot_name}: Hello {name}! How can I help?")
    elif "timing" in message or "open" in message or "hours" in message:
        print(f"{bot_name}: We are open 10 am to 8 pm, Monday to Saturday.")
    elif "fee" in message or "price" in message or "cost" in message:
        print(f"{bot_name}: Consultation fee is 2,000 PKR.")
    elif "where" in message or "location" in message or "address" in message:
        print(f"{bot_name}: We are on Main Road, near the city park.")
    elif "appointment" in message or "book" in message:
        print(f"{bot_name}: Call us or visit during opening hours to book an appointment.")
    else:
        # Fallback: count it and show the prompt Module 2 will send to an AI.
        unanswered_count += 1
        ai_prompt = f"You are the friendly assistant of {business_name}. Answer in 2 short lines: {message}"
        print(f"{bot_name}: I am not sure yet. In Module 2, an AI will answer: {ai_prompt}")

print("=" * 40)
print(f"Chat summary: {message_count} messages, {unanswered_count} unanswered.")
print(f"Complaints received: {complaint_count}")
