import random

def unknown():
    responses = [
        "I'm not sure what you're asking for.",
        "Can you please rephrase that?",
        "I'm sorry, I don't understand."
    ]
    return random.choice(responses)
