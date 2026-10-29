"""Task 2.1: AI Tutor.

Asks for a topic and a level, sends them to a local Ollama model through
LangChain, and prints the answer with the tokens used and the time taken.
Built for a tuition centre that wants explanations at the right level.
"""

from langchain.chat_models import init_chat_model

# strip() removes accidental spaces so the AI never sees messy text.
topic = input("Topic: ").strip()
level = input("Level (beginner or expert): ").strip()

# The system message sets the ROLE and the answer LENGTH. Without a length
# limit the AI writes long answers, which cost more tokens and time.
system_message = f"You are a friendly tutor. Explain at a {level} level in 3 short lines."

# Low temperature (0.2) makes answers focused and consistent, which is
# what we want when teaching facts.
llm = init_chat_model("gemma4:31b-cloud", model_provider="ollama", temperature=0.2)

response = llm.invoke([
    {"role": "system", "content": system_message},
    {"role": "user", "content": topic},
])

# Ollama reports time in nanoseconds, so we divide by 1 billion for seconds.
total_tokens = response.usage_metadata["total_tokens"]
seconds = response.response_metadata["total_duration"] / 1_000_000_000

print("=" * 40)
print(response.text)
print("=" * 40)
print(f"{total_tokens} tokens in {seconds:.1f} seconds")