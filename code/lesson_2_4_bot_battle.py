"""Task 2.4 stretch: Bot Battle.

Runs each test question through simple rules (Lesson 1.8 style) and through
the AI, prints both answers, and counts how many the rules could not answer.
"""

from langchain.chat_models import init_chat_model

llm = init_chat_model("gemma4:31b-cloud", model_provider="ollama", temperature=0.2)

# Facts keep the AI honest, so the comparison is fair.
system_message = (
    "You are the assistant of Sweet Crumbs bakery in Lahore. Open 9 am to 10 pm daily. "
    "Delivery 200 PKR, free from 3,000 PKR. Prices in PKR: cupcake 250, brownie 300, "
    "chocolate cake 1500. If something is not in these facts, say you do not know. "
    "Answer in 2 short lines."
)

test_questions = [
    "What are your hours?",
    "Where are you located?",
    "Do you deliver to my area?",
    "How much is a cupcake?",
    "my order is late",
    "Do you make sugar-free cakes?",
    "Can I order a cake for a wedding?",
    "Which cake is best?",
]

rules_unanswered = 0

for question in test_questions:
    text = question.strip().lower()

    # Same idea as Lesson 1.8: complaint first, then the other intents.
    # " late" has a space before it so "chocolate" never counts as a complaint.
    if " late" in " " + text:
        rule_answer = "Sorry about that. A manager will call you within 1 hour."
    elif "hours" in text or "open" in text:
        rule_answer = "We are open 9 am to 10 pm, every day."
    elif "where" in text or "located" in text:
        rule_answer = "We are in Lahore."
    elif "deliver" in text:
        rule_answer = "Delivery is 200 PKR, free from 3,000 PKR."
    elif "price" in text or "how much" in text:
        rule_answer = "Cupcake 250, brownie 300, chocolate cake 1,500 PKR."
    else:
        rule_answer = "(no rule matched)"
        rules_unanswered += 1

    response = llm.invoke([
        {"role": "system", "content": system_message},
        {"role": "user", "content": question},
    ])

    print(f"Q: {question}")
    print(f"   Rules: {rule_answer}")
    print(f"   AI:    {response.text.strip()}")

print("=" * 50)
print(f"{len(test_questions)} questions, rules could not answer {rules_unanswered}.")