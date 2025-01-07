import streamlit as st
import json
import os
import random

# Base directories for lesson/chapter selection
directories = {
    "Data Management": "DataMan",  # Map logical name to folder name
    "OSDS": "OSDS"
}

# Helper function to get lessons or chapters
def get_lessons_or_chapters(directory):
    try:
        items = os.listdir(directory)
        lessons = [item for item in items if os.path.isfile(os.path.join(directory, item)) and item.endswith('.json')]
        return sorted(lessons)
    except FileNotFoundError:
        st.error(f"Directory '{directory}' not found.")
        return []

# Load questions from a selected JSON file
def load_questions(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data.get("questions", [])
    except FileNotFoundError:
        st.error(f"File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        st.error(f"File '{file_path}' contains invalid JSON.")
        return []

# Flatten the data and randomize the order of the questions
def get_questions(data):
    questions = [q for q in data]
    random.shuffle(questions)
    return questions

# Check if session state variables are initialized
if "selection_screen" not in st.session_state:
    st.session_state.selection_screen = True
if "questions" not in st.session_state:
    st.session_state.questions = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answer_checked" not in st.session_state:
    st.session_state.answer_checked = False

if st.session_state.selection_screen:
    # Directory selection
    selected_directory = st.sidebar.selectbox("Select Directory", list(directories.keys()))
    
    # Lesson or chapter selection
    base_path = directories[selected_directory]
    lessons_or_chapters = get_lessons_or_chapters(base_path)
    if not lessons_or_chapters:
        st.warning(f"No valid JSON lessons found in {selected_directory}.")
    else:
        selected_file = st.sidebar.selectbox("Select Lesson/Chapter", lessons_or_chapters)

        if selected_file and st.button("Start Quiz"):
            file_path = os.path.join(base_path, selected_file)
            questions = load_questions(file_path)
            if questions:
                st.session_state.questions = get_questions(questions)
                st.session_state.selection_screen = False
                st.session_state.question_index = 0
                st.session_state.score = 0
                st.session_state.answer_checked = False
else:
    # Get the current question
    current_question = st.session_state.questions[st.session_state.question_index]

    # Display question and options
    st.subheader(f"Question {st.session_state.question_index + 1}")
    st.write(current_question["question"])

    # Show answer choices
    choices = current_question["options"]
    selected_option = st.radio("Options", choices, key=st.session_state.question_index)

    # Check answer
    if st.button("Check Answer"):
        if selected_option == current_question["answer"]:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! The correct answer was: {current_question['answer']}")
        st.session_state.answer_checked = True

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.question_index > 0 and st.button("Previous Question"):
            st.session_state.question_index -= 1
            st.session_state.answer_checked = False

    with col2:
        if st.session_state.answer_checked and st.button("Next Question"):
            st.session_state.question_index += 1
            if st.session_state.question_index >= len(st.session_state.questions):
                st.session_state.question_index = 0
                st.session_state.questions = get_questions(st.session_state.questions)  # Re-randomize questions
            st.session_state.answer_checked = False

    with col3:
        if st.button("Back to Selection Screen"):
            st.session_state.selection_screen = True
            st.session_state.questions = []
            st.session_state.question_index = 0
            st.session_state.score = 0

    # Display score
    st.write(f"Your current score: {st.session_state.score}/{len(st.session_state.questions)}")
