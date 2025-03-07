"""
Quiz content for the AI Learning Platform.

This module contains the quiz questions for each lesson, organized into a dictionary
structure for easy access and management.
"""

# Define the quiz questions
quizzes = {
    1: {  # Lesson 1: Introduction to AI and Machine Learning
        "title": "Quiz: Introduction to AI and Machine Learning",
        "description": "Test your understanding of AI and machine learning fundamentals.",
        "questions": [
            {
                "question": "What is artificial intelligence?",
                "type": "multiple_choice",
                "options": [
                    "Computer systems designed to perform creative tasks only",
                    "Computer systems designed to perform tasks that typically require human intelligence",
                    "The study of robots and how they move",
                    "Software that can only solve mathematical problems"
                ],
                "correct_answer": 1,  # 0-indexed
                "explanation": "Artificial Intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence, such as problem-solving, language understanding, pattern recognition, and learning from experience."
            },
            {
                "question": "What is the main difference between AI and machine learning?",
                "type": "multiple_choice",
                "options": [
                    "AI is older than machine learning",
                    "Machine learning requires human supervision while AI doesn't",
                    "Machine learning is a subset of AI focused on learning from data",
                    "AI works with text while machine learning works with numbers"
                ],
                "correct_answer": 2,
                "explanation": "Machine learning is a subset of AI that focuses specifically on allowing computers to learn from data without being explicitly programmed for every task."
            },
            {
                "question": "In supervised learning, what is provided to the computer?",
                "type": "multiple_choice",
                "options": [
                    "Only the input data",
                    "Input data with corresponding labels or answers",
                    "A set of rules to follow",
                    "Rewards and penalties"
                ],
                "correct_answer": 1,
                "explanation": "In supervised learning, the computer is provided with labeled examples (input data with corresponding answers), allowing it to learn the relationship between inputs and outputs."
            },
            {
                "question": "Which of these is NOT an example of AI in daily life?",
                "type": "multiple_choice",
                "options": [
                    "Voice assistants like Siri or Alexa",
                    "Traffic predictions in navigation apps",
                    "A basic calculator performing arithmetic",
                    "Recommendations on streaming services"
                ],
                "correct_answer": 2,
                "explanation": "A basic calculator performs fixed operations based on explicit programming without learning or adapting. The other examples involve AI systems that process complex data, recognize patterns, or learn from user behavior."
            },
            {
                "question": "How might AI assist in law enforcement?",
                "type": "multiple_select",
                "options": [
                    "Analyzing large volumes of data for investigations",
                    "Completely replacing human judgment in legal decisions",
                    "Automating routine paperwork",
                    "Identifying patterns in criminal activity"
                ],
                "correct_answers": [0, 2, 3],
                "explanation": "AI can help with data analysis, automating routine tasks, and identifying patterns, but it should not completely replace human judgment in legal decisions."
            }
        ]
    },
    
    2: {  # Lesson 2: Large Language Models: The Basics
        "title": "Quiz: Large Language Models: The Basics",
        "description": "Test your understanding of what LLMs are and how they work.",
        "questions": [
            {
                "question": "Why are they called 'Large' Language Models?",
                "type": "multiple_select",
                "options": [
                    "They're trained on enormous datasets",
                    "They can only generate long responses",
                    "They contain billions or trillions of parameters",
                    "They require significant computing power"
                ],
                "correct_answers": [0, 2, 3],
                "explanation": "LLMs are called 'large' because they're trained on enormous datasets, contain billions or trillions of parameters, and require significant computing power to train and run."
            },
            {
                "question": "At its most basic level, what task do LLMs perform?",
                "type": "multiple_choice",
                "options": [
                    "Image recognition",
                    "Predicting the next word in a sequence",
                    "Voice synthesis",
                    "Video analysis"
                ],
                "correct_answer": 1,
                "explanation": "At their core, LLMs work by predicting what text should come next in a sequence based on patterns they've learned from their training data."
            },
            {
                "question": "Which of these is NOT a capability of current LLMs?",
                "type": "multiple_choice",
                "options": [
                    "Generating human-like text responses",
                    "Summarizing information",
                    "Having real-world experiences and emotions",
                    "Translating languages"
                ],
                "correct_answer": 2,
                "explanation": "LLMs don't have real-world experiences or emotions. They simulate understanding based on patterns in text but don't actually experience the world or have feelings."
            },
            {
                "question": "What is a limitation of LLMs?",
                "type": "multiple_select",
                "options": [
                    "They can generate incorrect information confidently",
                    "They have a knowledge cutoff date",
                    "They can only process short inputs",
                    "They can exhibit biases present in their training data"
                ],
                "correct_answers": [0, 1, 3],
                "explanation": "LLMs can generate incorrect information confidently, have knowledge limited to their training cutoff date, and can exhibit biases present in their training data. Many modern LLMs can process fairly long inputs."
            },
            {
                "question": "How might LLMs assist in law enforcement contexts?",
                "type": "multiple_select",
                "options": [
                    "Drafting reports",
                    "Making arrest decisions automatically",
                    "Summarizing case notes or witness statements",
                    "Explaining complex legal concepts in simple terms"
                ],
                "correct_answers": [0, 2, 3],
                "explanation": "LLMs can help with drafting reports, summarizing information, and explaining concepts. However, they should not be used to make critical decisions like arrests automatically."
            }
        ]
    },
    
    3: {  # Lesson 3: How LLMs Process Information
        "title": "Quiz: How LLMs Process Information",
        "description": "Test your understanding of tokenization, embeddings, and attention mechanisms.",
        "questions": [
            {
                "question": "What is tokenization in the context of LLMs?",
                "type": "multiple_choice",
                "options": [
                    "Converting text to images",
                    "Breaking text into smaller pieces that the model can process",
                    "Encrypting sensitive information",
                    "The process of training an LLM"
                ],
                "correct_answer": 1,
                "explanation": "Tokenization is the process of breaking text down into smaller pieces called tokens, which are the basic units the model works with."
            },
            {
                "question": "What are tokens in an LLM?",
                "type": "multiple_select",
                "options": [
                    "Always complete words",
                    "Parts of words",
                    "Individual characters",
                    "Always sentences"
                ],
                "correct_answers": [1, 2],
                "explanation": "Tokens can be parts of words or individual characters. They are not always complete words or sentences."
            },
            {
                "question": "What is the purpose of embeddings in LLMs?",
                "type": "multiple_choice",
                "options": [
                    "To compress text to save storage space",
                    "To convert tokens into numerical representations that capture meaning",
                    "To encrypt sensitive information",
                    "To speed up the model's response time"
                ],
                "correct_answer": 1,
                "explanation": "Embeddings convert tokens into numerical representations in a high-dimensional space, allowing the model to capture relationships and meaning between words."
            },
            {
                "question": "In the context of LLMs, what does the attention mechanism do?",
                "type": "multiple_choice",
                "options": [
                    "Ensures the model doesn't fall asleep while processing",
                    "Helps the model decide which parts of the input text are most relevant",
                    "Catches grammatical errors in the output",
                    "Monitors the user's engagement with the model"
                ],
                "correct_answer": 1,
                "explanation": "The attention mechanism helps the model decide which parts of the input text are most relevant for generating the next word, allowing it to focus on context."
            },
            {
                "question": "What is the correct sequence when an LLM processes your prompt?",
                "type": "ordering",
                "options": [
                    "Text is broken into tokens",
                    "Tokens are converted to embeddings",
                    "The attention mechanism identifies important relationships",
                    "The model predicts the most likely next token",
                    "The process repeats for each new token"
                ],
                "correct_order": [0, 1, 2, 3, 4],
                "explanation": "When processing a prompt, the LLM first breaks the text into tokens, converts them to embeddings, uses attention to identify relationships, predicts the next token, and repeats this process until the response is complete."
            }
        ]
    },
    
    4: {  # Lesson 4: The Art of Prompting
        "title": "Quiz: The Art of Prompting",
        "description": "Test your understanding of effective prompting techniques.",
        "questions": [
            {
                "question": "What is prompting in the context of LLMs?",
                "type": "multiple_choice",
                "options": [
                    "Forcing the model to respond quickly",
                    "The input text you provide to get a desired response",
                    "Correcting the model when it makes mistakes",
                    "Restarting the model when it freezes"
                ],
                "correct_answer": 1,
                "explanation": "Prompting is how we communicate with LLMs - it's the input text you provide to the model to get a desired response."
            },
            {
                "question": "Which of these prompts demonstrates the 'Be Clear and Specific' principle?",
                "type": "multiple_choice",
                "options": [
                    "Tell me about reports.",
                    "Give me information.",
                    "Explain how to write a detailed police incident report for a residential burglary, including the key sections that should be included.",
                    "Write something about police work."
                ],
                "correct_answer": 2,
                "explanation": "The third option is clear and specific about what information is needed - it specifies the type of report, the incident type, and asks for key sections to include."
            },
            {
                "question": "Which advanced prompting strategy involves giving the LLM a specific perspective to take?",
                "type": "multiple_choice",
                "options": [
                    "Few-Shot Learning",
                    "Role Prompting",
                    "Step-by-Step Guidance",
                    "Format Specification"
                ],
                "correct_answer": 1,
                "explanation": "Role prompting involves framing your prompt by giving the LLM a specific role or perspective to take when generating a response."
            },
            {
                "question": "What is 'Few-Shot Learning' in prompting?",
                "type": "multiple_choice",
                "options": [
                    "Asking the model to learn a new skill with minimal training",
                    "Providing examples of what you want in your prompt",
                    "Limiting the model to short responses",
                    "Asking very simple questions first"
                ],
                "correct_answer": 1,
                "explanation": "Few-Shot Learning involves providing examples of what you want in your prompt to guide the model's response style and format."
            },
            {
                "question": "Which of these are common prompting pitfalls?",
                "type": "multiple_select",
                "options": [
                    "Being too vague",
                    "Information overload",
                    "Assuming background knowledge",
                    "Not iterating based on responses"
                ],
                "correct_answers": [0, 1, 2, 3],
                "explanation": "All of these are common pitfalls when prompting LLMs. Being vague, providing too much information, assuming the model knows specific context, and not refining prompts based on responses can all lead to suboptimal results."
            }
        ]
    },
    
    5: {  # Lesson 5: Practical Applications and Responsible Use
        "title": "Quiz: Practical Applications and Responsible Use",
        "description": "Test your understanding of LLM applications and ethical considerations.",
        "questions": [
            {
                "question": "Which of these is an appropriate use of LLMs in law enforcement?",
                "type": "multiple_select",
                "options": [
                    "Drafting and formatting reports",
                    "Making final judgments about suspect guilt",
                    "Summarizing witness statements",
                    "Creating training scenarios and materials"
                ],
                "correct_answers": [0, 2, 3],
                "explanation": "LLMs are appropriate for drafting reports, summarizing information, and creating training materials. They should not make critical legal judgments like determining guilt."
            },
            {
                "question": "When using LLMs with case information, what is a critical consideration?",
                "type": "multiple_choice",
                "options": [
                    "Always use the most powerful model available",
                    "Include as much detail as possible for best results",
                    "Never input confidential information or personal data",
                    "Always accept the LLM's output without verification"
                ],
                "correct_answer": 2,
                "explanation": "Privacy and confidentiality are critical considerations. You should never input confidential information, personal data, or sensitive case details into public LLM systems."
            },
            {
                "question": "What should you always do with information generated by an LLM?",
                "type": "multiple_choice",
                "options": [
                    "Share it immediately with colleagues",
                    "Verify its accuracy, especially for facts, laws, and procedures",
                    "Assume it's completely accurate",
                    "Submit it without review"
                ],
                "correct_answer": 1,
                "explanation": "Always verify LLM-generated information, especially facts, laws, and procedures, as LLMs can sometimes present incorrect information confidently."
            },
            {
                "question": "Which of these are best practices for professional use of LLMs?",
                "type": "multiple_select",
                "options": [
                    "Start with complex tasks to test the model's capabilities",
                    "Maintain human review of all AI-generated content",
                    "Use only secure, approved tools",
                    "Document when and how AI tools were used"
                ],
                "correct_answers": [1, 2, 3],
                "explanation": "Best practices include maintaining human review, using secure approved tools, and documenting AI usage. It's better to start with simple tasks rather than complex ones as you build experience."
            },
            {
                "question": "Why is it important to be aware of potential bias in LLM outputs?",
                "type": "multiple_choice",
                "options": [
                    "Because bias only affects certain topics",
                    "Because LLMs create random biases independent of their training",
                    "Because LLMs can reflect and sometimes amplify societal biases present in training data",
                    "Because bias only matters in academic settings"
                ],
                "correct_answer": 2,
                "explanation": "LLMs can reflect and sometimes amplify societal biases present in their training data. Being aware of this helps users review outputs for potential bias in language or conclusions."
            }
        ]
    },
    
    6: {  # Lesson 6: AI Ethics and Responsible Use in Law Enforcement
        "title": "Quiz: AI Ethics and Responsible Use in Law Enforcement",
        "description": "Test your understanding of ethical considerations when using AI in law enforcement contexts.",
        "questions": [
            {
                "question": "Why is transparency important when using AI in law enforcement?",
                "type": "multiple_select",
                "options": [
                    "To ensure AI-assisted processes can be explained in court",
                    "To make AI algorithms run faster",
                    "To document how AI tools are used in investigations",
                    "To reduce the cost of AI implementation"
                ],
                "correct_answers": [0, 2],
                "explanation": "Transparency in AI use for law enforcement is crucial for explaining processes in court and properly documenting how tools are used in investigations. This builds trust and accountability."
            },
            {
                "question": "What is 'data bias' in the context of AI systems?",
                "type": "multiple_choice",
                "options": [
                    "When AI systems perform differently across computer hardware",
                    "When training data doesn't represent the population it will be used on",
                    "When AI costs too much to implement properly",
                    "When AI systems are deliberately programmed with bias"
                ],
                "correct_answer": 1,
                "explanation": "Data bias occurs when the data used to train an AI system doesn't adequately represent the population the system will be used on, potentially leading to unfair or discriminatory outcomes."
            },
            {
                "question": "Which of these is a recommended best practice for addressing AI bias?",
                "type": "multiple_select",
                "options": [
                    "Maintain meaningful human review of AI-assisted decisions",
                    "Rely completely on AI for decisions to remove human bias",
                    "Regularly test systems for biased outcomes",
                    "Use the most complex AI available regardless of explainability"
                ],
                "correct_answers": [0, 2],
                "explanation": "Best practices for addressing AI bias include maintaining human oversight of AI-assisted decisions and regularly testing systems to identify and address biased outcomes."
            },
            {
                "question": "What ethical concern is associated with predictive policing AI?",
                "type": "multiple_choice",
                "options": [
                    "It's too expensive to implement properly",
                    "It requires too much computing power",
                    "It may reinforce patterns of over-policing in certain communities",
                    "It's too difficult for officers to understand"
                ],
                "correct_answer": 2,
                "explanation": "A major ethical concern with predictive policing is that it may reinforce existing patterns of over-policing in certain communities, creating a feedback loop where predictions become self-fulfilling."
            },
            {
                "question": "What is the correct order for a framework of responsible AI implementation?",
                "type": "ordering",
                "options": [
                    "Need Assessment: Define the problem to solve",
                    "Tool Selection: Choose appropriate tools",
                    "Risk Assessment: Evaluate potential risks",
                    "Policy Development: Create governance policies",
                    "Training: Ensure personnel are prepared",
                    "Auditing: Regularly review performance"
                ],
                "correct_order": [0, 1, 2, 3, 4, 5],
                "explanation": "A responsible AI implementation framework starts with clearly defining the problem (need assessment), then selects appropriate tools, evaluates risks, develops policies, trains personnel, and establishes regular auditing."
            }
        ]
    }
}

# Function to get quiz by ID
def get_quiz(quiz_id):
    """Get a specific quiz by ID (which corresponds to lesson ID)"""
    return quizzes.get(quiz_id, None)

# Function to get all quiz titles
def get_quiz_titles():
    """Get a list of all quiz titles with their IDs"""
    return [(quiz_id, data["title"]) for quiz_id, data in quizzes.items()]

# Function to calculate score
def calculate_quiz_score(quiz_id, user_answers):
    """Calculate the score for a quiz based on user answers"""
    quiz = get_quiz(quiz_id)
    if not quiz:
        return 0
    
    total_questions = len(quiz["questions"])
    correct_count = 0
    
    for i, question in enumerate(quiz["questions"]):
        if i not in user_answers:
            continue
            
        user_answer = user_answers[i]
        
        if question["type"] == "multiple_choice":
            if user_answer == question["correct_answer"]:
                correct_count += 1
                
        elif question["type"] == "multiple_select":
            if set(user_answer) == set(question["correct_answers"]):
                correct_count += 1
                
        elif question["type"] == "ordering":
            if user_answer == question["correct_order"]:
                correct_count += 1
    
    if total_questions > 0:
        return (correct_count / total_questions) * 100
    return 0 