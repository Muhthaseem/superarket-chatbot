import json
import random
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Load intents from the JSON file
with open('intents.json') as file:
    intents = json.load(file)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculate the percentage of recognised words
    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}
    best_match_tag = None

    for intent in intents['intents']:
        tag = intent['tag']
        patterns = intent['patterns']
        required_words = intent.get('required_words', [])
        for pattern in patterns:
            pattern_words = re.split(r'\s+|[,;?!.-]\s*', pattern.lower())
            probability = message_probability(message, pattern_words, single_response=False, required_words=required_words)
            if tag in highest_prob_list:
                highest_prob_list[tag] = max(highest_prob_list[tag], probability)
            else:
                highest_prob_list[tag] = probability

    best_match_tag = max(highest_prob_list, key=highest_prob_list.get)
    print(f"Message probabilities: {highest_prob_list}")  # Debugging information

    if highest_prob_list[best_match_tag] < 1:
        return "I'm sorry, I didn't understand that.", None

    response = random.choice(next(intent['responses'] for intent in intents['intents'] if intent['tag'] == best_match_tag))
    return response, best_match_tag

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response, tag = check_all_messages(split_message)

    if tag in ["items", "shelf_locations"]:
        for intent in intents['intents']:
            if intent['tag'] == "shelf_locations":
                for pattern, shelf_response in zip(intent['patterns'], intent['responses']):
                    pattern_words = re.split(r'\s+|[,;?!.-]\s*', pattern.lower())
                    if any(word in split_message for word in pattern_words if word):  # Ensure any pattern words match
                        return shelf_response

    return response

def send_message(event=None):
    user_input = user_input_entry.get().strip()
    if user_input.lower() == 'exit':
        root.quit()
    response = get_response(user_input)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"You: {user_input}\n", "user")
    chat_log.insert(tk.END, f"Bot: {response}\n\n", "bot")
    chat_log.config(state=tk.DISABLED)
    user_input_entry.delete(0, tk.END)

def exit_app():
    root.quit()

def restart_app():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete('1.0', tk.END)  # Clear the chat log
    chat_log.insert(tk.END, "Bot: Welcome to ALPHA supermarket !!!\n\n", "bot")
    chat_log.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Supermarket Chatbot")

# Set dark mode
root.configure(bg='#2e2e2e')

# Create chat history window with WhatsApp-like styling
chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, bg='#1e1e1e', fg='#d3d3d3', padx=10, pady=10)
chat_log.tag_config('user', foreground='#25d366', font=("Helvetica", 12, "bold"), spacing1=10, spacing3=10)
chat_log.tag_config('bot', foreground='#34b7f1', font=("Helvetica", 12, "bold"), spacing1=10, spacing3=10)
chat_log.pack(padx=10, pady=10)

# Welcome message
chat_log.config(state=tk.NORMAL)
chat_log.insert(tk.END, "Bot: Welcome to ALPHA supermarket !!!\n\n", "bot")
chat_log.config(state=tk.DISABLED)

# Create user input entry field with WhatsApp-like styling
user_input_entry = tk.Entry(root, width=50, bg='#333333', fg='#ffffff', insertbackground='white', font=("Helvetica", 12))
user_input_entry.pack(padx=10, pady=(0, 10))

# Create send button with WhatsApp-like styling
send_button = tk.Button(root, text="Send", command=send_message, bg='#128c7e', fg='#ffffff', activebackground='#075e54', font=("Helvetica", 12, "bold"))
send_button.pack(padx=10, pady=10)

# Create Exit and Restart buttons
button_frame = tk.Frame(root, bg='#2e2e2e')
button_frame.pack(pady=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit_app, bg='#d9534f', fg='#ffffff', activebackground='#c9302c', font=("Helvetica", 12, "bold"))
exit_button.pack(side=tk.LEFT, padx=(0, 10))

restart_button = tk.Button(button_frame, text="Restart", command=restart_app, bg='#5bc0de', fg='#ffffff', activebackground='#31b0d5', font=("Helvetica", 12, "bold"))
restart_button.pack(side=tk.RIGHT, padx=(10, 0))

# Bind Enter key to send_message function
root.bind('<Return>', send_message)

# Start the main loop for the GUI
root.mainloop()
