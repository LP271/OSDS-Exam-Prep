import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# Check if quiz_data.json exists
file_path = "quiz_data.json"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found. Make sure it's in the same directory as main.py.")

# Load questions from quiz_data.json
with open(file_path, "r") as file:
    quiz_data = json.load(file)

questions = quiz_data["questions"]

# Shuffle the questions to make the order random
random.shuffle(questions)

# Variable to track the current question index
current_question = 0
score = 0

def check_answer(selected_option):
    global current_question, score
    is_correct = questions[current_question]["options"][selected_option] == questions[current_question]["answer"]
    if is_correct:
        score += 1
        result_label.config(text="Correct!", fg="lime")
    else:
        result_label.config(text=f"Wrong! Correct answer: {questions[current_question]['answer']}", fg="red")
    
    # Enable the "Next" button
    next_button.config(state=tk.NORMAL)

def next_question():
    global current_question
    current_question += 1  # Increment the question index
    if current_question < len(questions):
        load_question(current_question)
        result_label.config(text="")  # Clear the result label
        next_button.config(state=tk.DISABLED)  # Disable the "Next" button
    else:
        show_score()

def load_question(question_index):
    question = questions[question_index]
    
    # Update the question text
    question_label.config(text=question["question"])
    
    # Update the button text with options
    for i, option in enumerate(question["options"]):
        option_buttons[i].config(text=option, state=tk.NORMAL)
    
    # Disable buttons if the options are fewer than the total buttons
    for i in range(len(question["options"]), len(option_buttons)):
        option_buttons[i].config(state=tk.DISABLED)

def show_score():
    messagebox.showinfo("Quiz Completed", f"Your final score is: {score}/{len(questions)}")
    window.quit()

# Create the main window with a dark theme
window = tk.Tk()
window.title("Quiz App")
window.config(bg="#121212")  # Dark background color

# Create the question label
question_label = tk.Label(window, text="", font=("Arial", 16), width=50, height=2, anchor="w", fg="white", bg="#121212", wraplength=600)
question_label.pack(pady=20)

# Create the buttons for options
option_buttons = []
for i in range(4):
    button = tk.Button(
        window, text="", font=("Arial", 14), width=50, height=2, 
        command=lambda i=i: check_answer(i), bg="#1E1E1E", fg="white", activebackground="#333333", activeforeground="white", wraplength=600
    )
    button.pack(pady=5)
    option_buttons.append(button)

# Create a label to display results (correct or wrong)
result_label = tk.Label(window, text="", font=("Arial", 14), bg="#121212", fg="white")
result_label.pack(pady=10)

# Create the "Next" button
next_button = tk.Button(window, text="Next", font=("Arial", 14), width=20, height=2, command=next_question, state=tk.DISABLED, bg="#1E1E1E", fg="white", activebackground="#333333", activeforeground="white")
next_button.pack(pady=20)

# Load the first question
load_question(current_question)

# Run the Tkinter event loop
window.mainloop()