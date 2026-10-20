"""Task 1.6: Prompt Cleaner.

Cleans a messy name and question, measures them, checks for the word
"python", and builds a safe, size-limited prompt for an AI.
"""

raw_name = input("Your name: ")
raw_question = input("Your question: ")

print(f"Your name: {raw_name}")
print(f"Your question: {raw_question}")

# strip() removes extra spaces and title()/capitalize() fix random capitals,
# so the AI always receives tidy text.
name = raw_name.strip().title()
question = raw_question.strip().capitalize()

# Stretch: hide a bad word before building the prompt
question = question.replace("stupid", "***")

# Models are billed in tokens, and 1 token is roughly 4 characters,
# so characters / 4 gives a quick cost-size estimate.
characters = len(question)
estimated_tokens = round(characters / 4)
estimated_cost = estimated_tokens / 1000 * 0.5   # example price per 1K tokens

# lower() makes the check work for PYTHON, Python or python.
mentions_python = "python" in question.lower()

print("=" * 40)
print(f"Cleaned question: {question}")
print(f"Characters: {characters}, about {estimated_tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print(f"Estimated cost: {estimated_cost:.2f} PKR")
print("=" * 40)

# [:150] slicing limits the question length so a huge message
# cannot create an expensive prompt.
prompt = f"""You are a friendly Python tutor.
Greet {name} by name and answer in 3 short lines.
Question: {question[:150]}"""
print(prompt)