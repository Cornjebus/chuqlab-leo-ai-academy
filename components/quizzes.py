import streamlit as st
import random
from content.quiz_content import get_quiz, get_quiz_titles, calculate_quiz_score
from auth.user_db import UserDatabase

def display_quiz():
    """Display the quiz page with selection and questions"""
    st.header("🧠 Quizzes")
    
    # Get all quiz titles
    quiz_titles = get_quiz_titles()
    
    # Get the current user
    username = st.session_state.get("username")
    
    # Initialize user database
    user_db = UserDatabase()
    
    # Get quiz history
    if username:
        user_data = user_db.get_user_data(username)
        quiz_scores = user_data.get('quiz_scores', {})
    else:
        quiz_scores = {}
    
    # Create quiz selection
    st.subheader("Select a Quiz")
    
    # Convert quiz_titles list to options for the selectbox
    quiz_options = []
    for quiz_id, title in quiz_titles:
        # Add score if available
        score_text = f" (Score: {quiz_scores.get(str(quiz_id), {}).get('score', 0)}%)" if str(quiz_id) in quiz_scores else ""
        quiz_options.append(f"{title}{score_text}")
    
    # Select quiz
    selected_index = st.selectbox(
        "Choose a quiz:", 
        range(len(quiz_options)),
        format_func=lambda i: quiz_options[i]
    )
    
    # Get the selected quiz ID
    selected_quiz_id = quiz_titles[selected_index][0]
    
    # Initialize or get quiz state
    if "quiz_state" not in st.session_state or st.session_state.quiz_state.get("quiz_id") != selected_quiz_id:
        st.session_state.quiz_state = {
            "quiz_id": selected_quiz_id,
            "started": False,
            "completed": False,
            "answers": {},
            "shuffled_options": {},
            "score": 0
        }
    
    # Display quiz information
    quiz = get_quiz(selected_quiz_id)
    if not quiz:
        st.error(f"Quiz {selected_quiz_id} not found.")
        return
    
    st.write(quiz["description"])
    
    # Start quiz button
    if not st.session_state.quiz_state["started"]:
        if st.button("Start Quiz"):
            st.session_state.quiz_state["started"] = True
            
            # Shuffle options for multiple choice and multiple select questions
            shuffled_options = {}
            for i, question in enumerate(quiz["questions"]):
                if question["type"] in ["multiple_choice", "multiple_select"]:
                    # Create shuffled indices
                    original_indices = list(range(len(question["options"])))
                    random.shuffle(original_indices)
                    shuffled_options[i] = original_indices
                    
                    # Update correct answer mapping for multiple choice
                    if question["type"] == "multiple_choice":
                        correct = question["correct_answer"]
                        # Find where the correct answer went in the shuffle
                        for j, orig_idx in enumerate(original_indices):
                            if orig_idx == correct:
                                question["shuffled_correct"] = j
                                break
                    
                    # Update correct answers mapping for multiple select
                    elif question["type"] == "multiple_select":
                        correct = question["correct_answers"]
                        # Find where each correct answer went in the shuffle
                        shuffled_correct = []
                        for orig_idx in correct:
                            for j, idx in enumerate(original_indices):
                                if idx == orig_idx:
                                    shuffled_correct.append(j)
                                    break
                        question["shuffled_correct"] = shuffled_correct
            
            st.session_state.quiz_state["shuffled_options"] = shuffled_options
            st.rerun()
    
    # Display quiz questions
    if st.session_state.quiz_state["started"] and not st.session_state.quiz_state["completed"]:
        st.subheader(quiz["title"])
        
        # Create a form for the quiz
        with st.form("quiz_form"):
            for i, question in enumerate(quiz["questions"]):
                st.markdown(f"### Question {i+1}: {question['question']}")
                
                shuffled_options = st.session_state.quiz_state["shuffled_options"].get(i, [])
                
                # Different input types based on question type
                if question["type"] == "multiple_choice":
                    # Display shuffled options
                    if shuffled_options:
                        options = [question["options"][idx] for idx in shuffled_options]
                    else:
                        options = question["options"]
                    
                    st.session_state.quiz_state["answers"][i] = st.radio(
                        f"Select one answer for question {i+1}:",
                        options=range(len(options)),
                        format_func=lambda j: options[j],
                        key=f"q{i}"
                    )
                
                elif question["type"] == "multiple_select":
                    # Display shuffled options
                    if shuffled_options:
                        options = [question["options"][idx] for idx in shuffled_options]
                    else:
                        options = question["options"]
                    
                    st.session_state.quiz_state["answers"][i] = st.multiselect(
                        f"Select all that apply for question {i+1}:",
                        options=range(len(options)),
                        format_func=lambda j: options[j],
                        key=f"q{i}"
                    )
                
                elif question["type"] == "ordering":
                    # For ordering questions, we use a different approach
                    # In a real app, you might want a drag-and-drop interface
                    options = question["options"]
                    order = []
                    
                    st.write("Arrange in the correct order (select items in the correct sequence):")
                    remaining = list(range(len(options)))
                    
                    # Create a sequence of selectboxes
                    for j in range(len(options)):
                        # Filter out already selected options
                        available = [idx for idx in remaining]
                        
                        if available:
                            selection = st.selectbox(
                                f"Position {j+1}:",
                                options=available,
                                format_func=lambda idx: options[idx],
                                key=f"q{i}_pos{j}"
                            )
                            order.append(selection)
                            remaining.remove(selection)
                    
                    st.session_state.quiz_state["answers"][i] = order
                
                st.markdown("---")
            
            # Submit button
            submitted = st.form_submit_button("Submit Answers")
            
            if submitted:
                # Calculate score
                score = calculate_quiz_score_with_shuffled(quiz, st.session_state.quiz_state)
                st.session_state.quiz_state["score"] = score
                st.session_state.quiz_state["completed"] = True
                
                # Save score if user is logged in
                if username:
                    user_db.save_quiz_score(username, str(selected_quiz_id), score)
                
                st.rerun()
    
    # Display quiz results
    if st.session_state.quiz_state["completed"]:
        score = st.session_state.quiz_state["score"]
        
        # Display score with appropriate feedback
        if score >= 80:
            st.success(f"🎉 Great job! Your score: {score:.1f}%")
        elif score >= 60:
            st.warning(f"👍 Good effort! Your score: {score:.1f}%")
        else:
            st.error(f"📚 Keep learning! Your score: {score:.1f}%")
        
        # Display correct answers and explanations
        st.subheader("Review Your Answers")
        
        for i, question in enumerate(quiz["questions"]):
            st.markdown(f"### Question {i+1}: {question['question']}")
            
            user_answer = st.session_state.quiz_state["answers"].get(i)
            shuffled_options = st.session_state.quiz_state["shuffled_options"].get(i, [])
            
            # Show the user's answer and the correct answer
            if question["type"] == "multiple_choice":
                options = question["options"]
                
                # Get the correct option index, accounting for shuffling
                if shuffled_options:
                    # Convert the user's shuffled selection back to original index
                    original_user_answer = shuffled_options[user_answer] if user_answer is not None else None
                    
                    # Display options with correct/incorrect marking
                    for j, orig_idx in enumerate(shuffled_options):
                        prefix = "✅ " if orig_idx == question["correct_answer"] else "❌ " if j == user_answer else "○ "
                        st.write(f"{prefix} {options[orig_idx]}")
                else:
                    # No shuffling case
                    for j, option in enumerate(options):
                        prefix = "✅ " if j == question["correct_answer"] else "❌ " if j == user_answer else "○ "
                        st.write(f"{prefix} {option}")
            
            elif question["type"] == "multiple_select":
                options = question["options"]
                
                # Get the correct options, accounting for shuffling
                if shuffled_options:
                    # Convert the user's shuffled selections back to original indices
                    original_user_answers = [shuffled_options[j] for j in user_answer] if user_answer else []
                    
                    # Display options with correct/incorrect marking
                    for j, orig_idx in enumerate(shuffled_options):
                        is_correct = orig_idx in question["correct_answers"]
                        was_selected = j in user_answer
                        
                        if is_correct and was_selected:
                            prefix = "✅ "  # Correct and selected
                        elif not is_correct and was_selected:
                            prefix = "❌ "  # Incorrect and selected
                        elif is_correct and not was_selected:
                            prefix = "⭕ "  # Correct but not selected
                        else:
                            prefix = "○ "  # Incorrect and not selected
                        
                        st.write(f"{prefix} {options[orig_idx]}")
                else:
                    # No shuffling case
                    for j, option in enumerate(options):
                        is_correct = j in question["correct_answers"]
                        was_selected = j in user_answer
                        
                        if is_correct and was_selected:
                            prefix = "✅ "
                        elif not is_correct and was_selected:
                            prefix = "❌ "
                        elif is_correct and not was_selected:
                            prefix = "⭕ "
                        else:
                            prefix = "○ "
                        
                        st.write(f"{prefix} {option}")
            
            elif question["type"] == "ordering":
                options = question["options"]
                correct_order = question["correct_order"]
                
                # Display the correct order
                st.write("Correct order:")
                for j, idx in enumerate(correct_order):
                    st.write(f"{j+1}. {options[idx]}")
                
                # Display the user's order
                if user_answer:
                    st.write("Your order:")
                    for j, idx in enumerate(user_answer):
                        prefix = "✅ " if idx == correct_order[j] else "❌ "
                        st.write(f"{prefix} {j+1}. {options[idx]}")
            
            # Show explanation
            with st.expander("Explanation"):
                st.write(question["explanation"])
            
            st.markdown("---")
        
        # Retry button
        if st.button("Retry Quiz"):
            st.session_state.quiz_state = {
                "quiz_id": selected_quiz_id,
                "started": False,
                "completed": False,
                "answers": {},
                "shuffled_options": {},
                "score": 0
            }
            st.rerun()

def calculate_quiz_score_with_shuffled(quiz, quiz_state):
    """Calculate the score for a quiz, accounting for shuffled options"""
    total_questions = len(quiz["questions"])
    correct_count = 0
    
    for i, question in enumerate(quiz["questions"]):
        if i not in quiz_state["answers"]:
            continue
            
        user_answer = quiz_state["answers"][i]
        shuffled_options = quiz_state["shuffled_options"].get(i, [])
        
        if question["type"] == "multiple_choice":
            if shuffled_options:
                # Get the original index that the user selected
                if user_answer is not None:
                    original_answer = shuffled_options[user_answer]
                    if original_answer == question["correct_answer"]:
                        correct_count += 1
            else:
                # No shuffling
                if user_answer == question["correct_answer"]:
                    correct_count += 1
                    
        elif question["type"] == "multiple_select":
            if shuffled_options:
                # Convert user's selected shuffle indices back to original indices
                original_answers = [shuffled_options[j] for j in user_answer] if user_answer else []
                if set(original_answers) == set(question["correct_answers"]):
                    correct_count += 1
            else:
                # No shuffling
                if set(user_answer) == set(question["correct_answers"]):
                    correct_count += 1
                    
        elif question["type"] == "ordering":
            if user_answer == question["correct_order"]:
                correct_count += 1
    
    if total_questions > 0:
        return (correct_count / total_questions) * 100
    return 0 