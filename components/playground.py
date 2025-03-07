import streamlit as st
import os
import json
import time
from utils.llm_service import get_llm_response, get_available_models
from utils.session_state import save_conversation

def display_playground():
    """Display the interactive LLM playground"""
    st.header("🚀 LLM Playground")
    
    st.markdown("""
    Welcome to the LLM Playground! This is where you can practice your prompting skills
    and see how the AI responds in real-time. Experiment with different prompting techniques,
    and see how they affect the results.
    """)
    
    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    if "prompt_templates" not in st.session_state:
        st.session_state.prompt_templates = load_prompt_templates()
        
    if "send_clicked" not in st.session_state:
        st.session_state.send_clicked = False
        
    if "save_clicked" not in st.session_state:
        st.session_state.save_clicked = False
    
    # Callback functions for buttons
    def on_send_click():
        st.session_state.send_clicked = True
        
    def on_save_click():
        st.session_state.save_clicked = True
        
    def on_reset_click():
        st.session_state.conversation = []
    
    # Create sidebar for settings
    with st.sidebar:
        st.subheader("Playground Settings")
        
        # Model selection
        models = get_available_models()
        selected_model = st.selectbox("Select Model", models, key="model_select")
        
        # Temperature slider (controls randomness)
        temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            step=0.1,
            key="temperature_slider",
            help="Higher values make output more random, lower values make it more focused and deterministic."
        )
        
        # Max tokens slider
        max_tokens = st.slider(
            "Max Response Length", 
            min_value=50, 
            max_value=1000, 
            value=250, 
            step=50,
            key="max_tokens_slider",
            help="Maximum number of tokens (roughly words) to generate."
        )
        
        # Reset conversation button
        st.button("Reset Conversation", key="reset_convo_btn", on_click=on_reset_click)
    
    # Create prompt template selection
    st.subheader("Prompt Templates")
    template_options = ["Create Your Own"] + list(st.session_state.prompt_templates.keys())
    selected_template = st.selectbox(
        "Choose a template or create your own:", 
        template_options,
        key="template_select"
    )
    
    # Display template content or custom input
    if selected_template == "Create Your Own":
        prompt = st.text_area(
            "Enter your prompt:",
            height=150,
            placeholder="Type your message to the AI here...",
            key="custom_prompt"
        )
    else:
        # Get template and fill in any placeholders
        template = st.session_state.prompt_templates[selected_template]
        
        # Display template description
        if "description" in template:
            st.info(template["description"])
        
        # Handle template with placeholders
        if "placeholders" in template and template["placeholders"]:
            # Collect values for each placeholder
            placeholder_values = {}
            for placeholder in template["placeholders"]:
                placeholder_values[placeholder] = st.text_input(
                    f"Enter {placeholder}:", 
                    key=f"placeholder_{placeholder}"
                )
            
            # Generate the prompt with filled placeholders
            prompt_template = template["prompt"]
            prompt = prompt_template
            
            # Replace placeholders with values
            for placeholder, value in placeholder_values.items():
                prompt = prompt.replace(f"{{{{{placeholder}}}}}", value)
            
            # Show the final prompt
            with st.expander("Preview Final Prompt"):
                st.markdown(prompt)
        else:
            # Template without placeholders
            prompt = template["prompt"]
            
            # Show the prompt
            with st.expander("Preview Prompt"):
                st.markdown(prompt)
    
    # Submit button
    st.button("Send", key="send_prompt_btn", on_click=on_send_click)
    
    # Handle send button click
    if st.session_state.send_clicked and prompt:
        # Add user message to conversation
        st.session_state.conversation.append({
            "role": "user",
            "content": prompt
        })
        
        # Show "thinking" message
        with st.spinner("AI is thinking..."):
            try:
                # Get response from LLM service
                response = get_llm_response(
                    prompt=prompt,
                    conversation_history=st.session_state.conversation[:-1],  # Exclude current message
                    model=selected_model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Add AI response to conversation
                if response:
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": response
                    })
                else:
                    st.error("Failed to get response from the LLM. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Reset the send_clicked flag
        st.session_state.send_clicked = False
        
        # Force refresh to show the updated conversation
        st.rerun()
    
    # Display conversation
    st.subheader("Conversation")
    
    if not st.session_state.conversation:
        st.info("Your conversation will appear here. Start by sending a message!")
    else:
        # Create a container for scrollable conversation
        conversation_container = st.container()
        with conversation_container:
            for message in st.session_state.conversation:
                if message["role"] == "user":
                    st.markdown(f"**You:**")
                    st.markdown(message["content"])
                else:
                    st.markdown(f"**AI:**")
                    st.markdown(message["content"])
                    
                st.markdown("---")
    
    # Save conversation section
    st.subheader("Save Your Conversation")
    
    # Only show if there are messages
    if st.session_state.conversation:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            conversation_title = st.text_input(
                "Conversation title:", 
                placeholder="My conversation",
                key="conversation_title"
            )
        
        with col2:
            st.button("Save Conversation", key="save_convo_btn", on_click=on_save_click)
        
        # Handle save button click
        if st.session_state.save_clicked:
            if conversation_title:
                username = st.session_state.get("username", "guest")
                if username != "guest":
                    # Use the session_state utility to save
                    conversation_id = save_conversation(
                        username, 
                        conversation_title, 
                        st.session_state.conversation
                    )
                    
                    if conversation_id:
                        st.success(f"Conversation saved successfully!")
                    else:
                        st.error("Failed to save conversation. Please try again.")
                else:
                    st.warning("Please log in to save conversations.")
            else:
                st.warning("Please provide a title for your conversation.")
                
            # Reset the save_clicked flag
            st.session_state.save_clicked = False
    
    # Prompt engineering tips
    with st.expander("Prompting Tips"):
        st.markdown("""
        ### Effective Prompting Techniques
        
        1. **Be Clear and Specific**
           - Instead of "Tell me about AI", try "Explain the differences between machine learning and deep learning in law enforcement applications"
        
        2. **Provide Context**
           - Include relevant background information the AI might need
        
        3. **Specify Format**
           - Request specific formats like bullet points, tables, or step-by-step instructions
        
        4. **Try Role Prompting**
           - "Act as an experienced detective analyzing this evidence..."
        
        5. **Use Few-Shot Learning**
           - Provide examples of the type of response you want
           
        Remember to experiment and iterate on your prompts!
        """)

def load_prompt_templates():
    """Load predefined prompt templates"""
    templates = {
        # Law Enforcement Applications
        "Report Writing Assistant": {
            "description": "Get help drafting or improving an incident or investigation report.",
            "prompt": "I need to write a detailed police report about the following incident: {{incident_description}}. Please provide a well-structured report that includes all necessary sections, uses professional language, and focuses on objective facts.",
            "placeholders": ["incident_description"]
        },
        "Witness Interview Questions": {
            "description": "Generate effective questions for interviewing a witness.",
            "prompt": "I need to interview a witness about the following incident: {{incident_type}}. Please generate 10 effective, open-ended questions that will help me gather complete and detailed information from the witness.",
            "placeholders": ["incident_type"]
        },
        "Legal Concept Explainer": {
            "description": "Get simple explanations of complex legal concepts.",
            "prompt": "Explain the legal concept of '{{legal_concept}}' in simple, easy-to-understand language that a non-legal professional would understand. Include 2-3 everyday examples that illustrate the concept.",
            "placeholders": ["legal_concept"]
        },
        "Community Outreach Program": {
            "description": "Generate ideas for community policing and outreach programs.",
            "prompt": "I'm looking to develop a new community outreach program focused on {{focus_area}} for our department that serves {{community_type}}. Please suggest a detailed program outline including: 1) Program name and tagline, 2) Key objectives, 3) Target participants, 4) Required resources, 5) Implementation timeline, 6) Success metrics.",
            "placeholders": ["focus_area", "community_type"]
        },

        # Personal Growth Templates
        "Personal Learning Plan": {
            "description": "Create a customized learning plan for any topic or skill.",
            "prompt": "I want to learn {{skill_topic}}. Create a detailed {{timeframe}}-month learning plan that fits around a full-time job. Include: 1) Weekly goals and milestones, 2) Recommended resources and materials, 3) Practice exercises, 4) Ways to measure progress, 5) Potential challenges and solutions.",
            "placeholders": ["skill_topic", "timeframe"]
        },
        "Career Development Strategy": {
            "description": "Get personalized career development advice and planning.",
            "prompt": "I'm currently working as a {{current_role}} and want to transition into {{target_role}}. Please create a career development strategy that includes: 1) Required skills and qualifications, 2) Learning resources, 3) Networking opportunities, 4) Portfolio/experience building suggestions, 5) Timeline for transition.",
            "placeholders": ["current_role", "target_role"]
        },

        # Business Applications
        "Business Plan Generator": {
            "description": "Generate a structured business plan outline.",
            "prompt": "I'm planning to start a {{business_type}} business. Create a detailed business plan outline that includes: 1) Executive summary points, 2) Market analysis requirements, 3) Financial projections framework, 4) Marketing strategy elements, 5) Operations plan, 6) Risk assessment categories.",
            "placeholders": ["business_type"]
        },
        "Marketing Content Strategy": {
            "description": "Develop a content marketing strategy.",
            "prompt": "Create a content marketing strategy for my {{business_description}} targeting {{target_audience}}. Include: 1) Content types and themes, 2) Posting schedule, 3) Platform-specific strategies, 4) Engagement tactics, 5) Success metrics, 6) Content ideas for the first month.",
            "placeholders": ["business_description", "target_audience"]
        },

        # AI Understanding & Ethics
        "AI Concept Explainer": {
            "description": "Get clear explanations of AI concepts.",
            "prompt": "Explain {{ai_concept}} in simple terms. Include: 1) Basic definition, 2) Real-world examples, 3) How it works, 4) Common applications, 5) Limitations or challenges. Use analogies to make it easier to understand.",
            "placeholders": ["ai_concept"]
        },
        "AI Ethics Analyzer": {
            "description": "Analyze ethical implications of AI applications.",
            "prompt": "Analyze the ethical implications of using AI for {{use_case}}. Consider: 1) Privacy concerns, 2) Fairness and bias issues, 3) Transparency requirements, 4) Social impact, 5) Recommended guidelines and safeguards.",
            "placeholders": ["use_case"]
        },
        "AI Implementation Plan": {
            "description": "Plan the implementation of AI in an organization.",
            "prompt": "Create an implementation plan for using AI in {{department_type}} to improve {{process_area}}. Include: 1) Current challenges, 2) Proposed AI solution, 3) Required resources, 4) Training needs, 5) Success metrics, 6) Risk mitigation strategies.",
            "placeholders": ["department_type", "process_area"]
        },

        # Professional Communication
        "Crisis Communication Script": {
            "description": "Create communication scripts for crisis situations.",
            "prompt": "I need help creating a communication script for responding to a {{crisis_type}} situation. The script should include: 1) Initial approach language, 2) De-escalation phrases, 3) Questions to assess the situation, 4) Reassurance statements, 5) Next steps explanation.",
            "placeholders": ["crisis_type"]
        },
        "Professional Document Improver": {
            "description": "Improve and polish any professional document.",
            "prompt": "Help me improve this {{document_type}}:\n\n{{document_text}}\n\nFocus on: 1) Clarity and conciseness, 2) Professional tone, 3) Structure and flow, 4) Grammar and style, 5) Impact and persuasiveness.",
            "placeholders": ["document_type", "document_text"]
        },

        # Training & Development
        "Training Scenario Developer": {
            "description": "Generate realistic training scenarios.",
            "prompt": "I need to develop a training scenario to help participants practice {{skill_area}}. Create a detailed, realistic scenario that: 1) Sets up a challenging situation, 2) Includes multiple decision points, 3) Provides necessary background information, 4) Lists learning objectives, 5) Includes debriefing questions.",
            "placeholders": ["skill_area"]
        },
        "Policy Simplifier": {
            "description": "Simplify complex policy language.",
            "prompt": "Simplify this policy text while maintaining its essential meaning:\n\n{{policy_text}}\n\nProvide: 1) Simplified version, 2) Key points summary, 3) Practical examples of application, 4) Common misconceptions to avoid.",
            "placeholders": ["policy_text"]
        }
    }
    
    return templates 