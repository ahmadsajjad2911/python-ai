"""AI Prompt Kit for a Local Business.

This tool asks a business owner 5 questions and prints 3 ready-to-use
AI prompts (marketing, customer service, growth) they can paste into
any AI such as Ollama, Claude or ChatGPT.

Made for small business owners who want AI help but don't know what to type.
"""

# Step 1: collect the 5 details. input() always returns a string.
business_name = input("Business name: ")
business_type = input("Business type (e.g. bakery): ")
city = input("City: ")
customers = input("Main customers (e.g. students, families): ")

# We convert the budget with int() because input() gives text, and a
# number is cleaner to show and safer to use later (e.g. for maths).
budget = int(input("Monthly budget in PKR: "))

# Step 2: show what the owner entered
print()
print(f"Business name: {business_name}")
print(f"Business type: {business_type}")
print(f"City: {city}")
print(f"Main customers: {customers}")
print(f"Monthly budget (PKR): {budget}")

# Step 3: header with the business name
print()
print("=" * 40)
print(f"   AI Prompt Kit for {business_name}")
print("=" * 40)

# Prompt 1: a good prompt names a role, task, audience and tone/number,
# so the AI gets specific instructions instead of guessing.
prompt_marketing = (
    f"Write a short Instagram post for {business_name}, a {business_type} "
    f"in {city}. Target {customers}. Friendly tone, 1 call to action."
)

# Prompt 2: giving the AI a role (manager) makes its reply sound
# professional, and naming the situation keeps the tone polite.
prompt_service = (
    f"You are the manager of {business_name}, a {business_type} in {city}. "
    f"Write a polite reply to an unhappy customer whose order arrived late. "
    f"Apologise and offer a small discount."
)

# Prompt 3: including the budget stops the AI from suggesting tools
# the owner cannot afford, and asking for exactly 3 ideas keeps it focused.
prompt_growth = (
    f"Suggest 3 low-cost AI ideas a {business_type} in {city} can use "
    f"to attract {customers} with a budget of {budget} PKR per month."
)

# Step 4: print the 3 prompts with clear separators
print()
print("[1] Marketing")
print(prompt_marketing)
print()
print("[2] Customer Service")
print(prompt_service)
print()
print("[3] Growth")
print(prompt_growth)
print()
print("=" * 40)