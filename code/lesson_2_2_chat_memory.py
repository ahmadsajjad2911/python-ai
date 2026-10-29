"""Task 2.2: Personal Tutor with Memory.

A chat tutor that remembers the conversation, but only the system message
plus the last 8 messages, so the cost does not grow forever.
Commands: /reset clears memory, /count shows memory size, bye exits.
"""

from langchain.chat_models import init_chat_model

llm = init_chat_model("gemma4:31b-cloud", model_provider="ollama", temperature=0.2)

# The system message is messages[0]. It sets the role and the answer length.
messages = [{"role": "system", "content": "You are a friendly tutor. Answer in 3 short lines or fewer."}]

# Stretch: a second list that keeps only the user's questions.
questions = []

print("Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    user_text = input("You: ").strip()
    command = user_text.lower()

    if command == "bye":
        print("Tutor: Goodbye!")
        break
    elif command == "/reset":
        # Keep ONLY the system message, otherwise the tutor loses its role.
        messages = [messages[0]]
        print("Tutor: Memory cleared.")
    elif command == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
    elif user_text == "":
        print("Tutor: Please type a question.")
    else:
        messages.append({"role": "user", "content": user_text})
        questions.append(user_text)

        # Trimming: keep the system message + the last 8 messages. The AI
        # only "remembers" what we send, so sending less saves tokens.
        messages = [messages[0]] + messages[1:][-8:]

        response = llm.invoke(messages)

        # The AI's reply must be saved too, or it forgets its own answers.
        messages.append({"role": "assistant", "content": response.text})

        print(f"Tutor: {response.text}")
        print(f"       (tokens sent: {response.usage_metadata['input_tokens']})")

# Stretch: summary of the questions asked
if len(questions) > 0:
    print(f"Questions asked: {len(questions)}")
    print(f"First question: {questions[0]}")
    print(f"Last question: {questions[-1]}")