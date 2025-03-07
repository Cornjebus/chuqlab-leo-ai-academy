# Chuqlab LEO AI Academy

An interactive Streamlit application designed to introduce law enforcement officers to AI and Large Language Models (LLMs).

## Overview

This application provides an accessible, user-friendly platform for law enforcement professionals to learn about AI and LLMs through:

- Structured, interactive lessons
- Hands-on exercises
- Interactive quizzes
- A live LLM playground for experimenting with prompts

## Features

- **User Authentication**: Secure login via email/password or Google OAuth
- **Educational Content**: Clear, non-technical explanations of AI and LLM concepts
- **Interactive Learning**: Step-by-step lessons with quizzes to reinforce concepts
- **LLM Playground**: Real-time interaction with LLMs to practice prompting skills
- **Progressive Learning Path**: Structured content from basic to more advanced concepts

## Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key (for LLM integration)
- Firebase project (for authentication)

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
   FIREBASE_PROJECT_ID=your_firebase_project_id
   ```
4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Create an account or log in
2. Navigate through lessons in the recommended order
3. Complete quizzes to test your understanding
4. Experiment with the LLM playground to practice your prompting skills

## Project Structure

- `app.py`: Main Streamlit application
- `auth/`: Authentication components
- `components/`: UI components and pages
- `content/`: Educational content and quizzes
- `utils/`: Utility functions for LLM integration and session management

## License

MIT 