"""Business Prompt Builder: asks for business details and prints a ready-to-use AI prompt."""

# input() always returns text, so we can drop the answers straight into an f-string
name = input("Your name: ")
business = input("Business type: ")
problem = input("Biggest problem: ")

# Stretch: int() because input() returns a string and the budget is a number
budget = int(input("Monthly budget (PKR): "))

print()
print(f"Welcome, {name}!")
print("--- Your AI Prompt ---")

# Build the prompt in one f-string so it can be pasted into any AI tool as-is
prompt = (
    f"Suggest 3 AI solutions for a {business} that struggles with {problem}. "
    f"Budget: {budget} PKR per month."
)
print(prompt)
