"""
Lesson content for the AI Learning Platform.

This module contains the educational content for each lesson, organized into a dictionary
structure for easy access and management.
"""

# Define the lesson content
lessons = {
    1: {
        "title": "Introduction to AI and Machine Learning",
        "description": "An overview of AI and machine learning fundamentals.",
        "content": """
        # Introduction to AI and Machine Learning
        
        ## What is Artificial Intelligence?
        
        Artificial Intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence. These include:
        
        - Problem-solving
        - Understanding language
        - Recognizing patterns
        - Learning from experience
        
        Think of AI as teaching computers to "think" and make decisions. However, computers don't really "think" like humans. Instead, they follow patterns and rules that we design or that they learn from data.
        
        ## What is Machine Learning?
        
        Machine Learning is a subset of AI that focuses on allowing computers to learn from data, without being explicitly programmed for every task.
        
        The basic idea is:
        1. Show the computer many examples
        2. The computer finds patterns in these examples
        3. The computer can then apply these patterns to new situations
        
        For instance, if you show a machine learning system thousands of pictures of cats and dogs with labels, it will learn to identify cats and dogs in new pictures.
        
        ## Types of Machine Learning
        
        ### Supervised Learning
        - The computer learns from labeled examples (like pictures with "cat" or "dog" labels)
        - Good for: Classification, prediction, and specific pattern recognition
        
        ### Unsupervised Learning
        - The computer finds patterns in unlabeled data
        - Good for: Discovering hidden patterns, grouping similar items
        
        ### Reinforcement Learning
        - The computer learns by receiving rewards or penalties
        - Good for: Gaming, robotics, and decision-making systems
        
        ## Real-World Applications
        
        AI and machine learning are already part of your daily life:
        
        - Voice assistants (Siri, Alexa)
        - Recommendations on streaming services
        - Fraud detection for your credit cards
        - Predictive text when you're typing messages
        - Traffic predictions in navigation apps
        
        In law enforcement, AI can help with:
        
        - Analyzing large volumes of data for investigations
        - Identifying patterns in criminal activity
        - Automating routine paperwork
        - Enhancing video analysis
        
        ## Key Takeaways
        
        - AI systems perform tasks that typically require human intelligence
        - Machine learning allows computers to learn from data and improve over time
        - AI is already widely used in many applications we interact with daily
        - Understanding basic AI concepts helps you use these tools more effectively
        """,
        "image_path": "static/images/ai_basics.png",
        "video_url": "https://www.youtube.com/embed/example1",
        "estimated_time": "15 minutes"
    },
    
    2: {
        "title": "Large Language Models: The Basics",
        "description": "Understanding what LLMs are and how they work.",
        "content": """
        # Large Language Models: The Basics
        
        ## What are Large Language Models?
        
        Large Language Models (LLMs) are a type of AI system trained on vast amounts of text data. They're called "large" because:
        
        1. They're trained on enormous datasets (trillions of words)
        2. They contain billions or even trillions of parameters (the "knobs" that get adjusted during learning)
        3. They require significant computing power to train and run
        
        Popular examples include:
        - GPT models (like ChatGPT)
        - Claude
        - LLaMA
        - Gemini
        
        ## How Do LLMs Work?
        
        At a high level, LLMs work by predicting what text should come next in a sequence. When you type a question or prompt, the LLM is essentially asking itself: "Based on all the text I've seen before, what would be the most likely way to respond?"
        
        The process works like this:
        
        1. **Training**: The model reads trillions of words from books, articles, websites, and other sources
        2. **Pattern Recognition**: The model learns patterns in language - which words tend to follow others, how ideas connect, etc.
        3. **Generation**: When given a prompt, the model generates a response based on the patterns it learned
        
        ## What LLMs Can and Cannot Do
        
        ### Capabilities:
        - Generate human-like text responses
        - Summarize information
        - Answer questions based on their training
        - Translate languages
        - Write different types of content (reports, stories, emails)
        - Explain complex topics in simple terms
        
        ### Limitations:
        - LLMs don't truly "understand" content the way humans do
        - They can generate incorrect information confidently
        - They have a knowledge cutoff date (they don't know events after their training)
        - They can exhibit biases present in their training data
        - They don't have real-world experiences or emotions
        
        ## The Impact of LLMs
        
        LLMs are transforming how we:
        - Search for information
        - Create content
        - Communicate with technology
        - Automate routine writing tasks
        - Learn new concepts
        
        For law enforcement, LLMs can:
        - Help draft reports
        - Summarize case notes or witness statements
        - Generate investigation questions
        - Explain complex legal concepts in simple terms
        - Assist with administrative tasks
        
        ## Key Takeaways
        
        - LLMs are AI systems trained on massive amounts of text data
        - They work by predicting what text should come next based on patterns they've learned
        - LLMs have impressive capabilities but also important limitations
        - Understanding these systems helps you use them more effectively and responsibly
        """,
        "image_path": "static/images/llm_basics.png",
        "video_url": "https://www.youtube.com/embed/example2",
        "estimated_time": "20 minutes"
    },
    
    3: {
        "title": "How LLMs Process Information",
        "description": "Understanding tokenization, embeddings, and attention.",
        "content": """
        # How LLMs Process Information
        
        ## Breaking Down Text: Tokenization
        
        Before an LLM can process text, it needs to break it down into smaller pieces called **tokens**. Think of tokens as the basic units the model works with.
        
        **What are tokens?**
        - Tokens can be words, parts of words, or even individual characters
        - In English, 1 token is roughly 3/4 of a word on average
        - For example, "hamburger" might be broken into tokens like "ham", "bur", and "ger"
        
        **Why tokenization matters:**
        - LLMs have token limits (e.g., 4,000 or 8,000 tokens)
        - More complex tokenization allows models to handle more languages efficiently
        - Understanding tokens helps you manage longer conversations with LLMs
        
        ## Understanding Text: Embeddings
        
        LLMs convert tokens into **embeddings** - numerical representations in a high-dimensional space.
        
        **What are embeddings?**
        - Think of them as converting words into points in space
        - Similar words or concepts appear close to each other in this space
        - For example, "police" and "officer" would be closer together than "police" and "banana"
        
        **Why embeddings matter:**
        - They help the model understand relationships between words
        - They allow the model to capture meaning, not just exact matches
        - They're crucial for understanding context and nuance
        
        ## Focusing on What Matters: Attention
        
        The **attention mechanism** is how LLMs decide which parts of the input text are most relevant for generating the next word.
        
        **How attention works:**
        - The model assigns "attention scores" to different parts of the prompt
        - Higher scores mean that part is more important for the current prediction
        - Multiple attention heads look at different relationships simultaneously
        
        **Why attention matters:**
        - It allows the model to focus on relevant context, even in long texts
        - It helps maintain consistency throughout the generated response
        - It's what enables LLMs to "remember" information from earlier in the conversation
        
        ## Putting It All Together
        
        When you send a prompt to an LLM, the process looks like this:
        
        1. Your text is broken into tokens
        2. Tokens are converted to embeddings
        3. The attention mechanism identifies important relationships
        4. The model predicts the most likely next token
        5. The process repeats for each new token until the response is complete
        
        ## Key Takeaways
        
        - Tokenization breaks text into manageable pieces for the model
        - Embeddings convert text into numerical representations that capture meaning
        - Attention mechanisms help the model focus on relevant parts of the input
        - Understanding these concepts helps you better interact with LLMs
        """,
        "image_path": "static/images/llm_processing.png",
        "video_url": "https://www.youtube.com/embed/example3",
        "estimated_time": "25 minutes"
    },
    
    4: {
        "title": "The Art of Prompting",
        "description": "Learning how to effectively communicate with LLMs.",
        "content": """
        # The Art of Prompting
        
        ## What is Prompting?
        
        **Prompting** is how we communicate with Large Language Models. A prompt is the input text you provide to the LLM to get a desired response.
        
        Effective prompting is crucial because:
        - It directly affects the quality of responses you receive
        - It can help avoid common LLM pitfalls
        - It allows you to leverage the model's capabilities more fully
        
        ## Basic Prompting Techniques
        
        ### 1. Be Clear and Specific
        
        **Instead of:** "Tell me about reports."
        
        **Better:** "Explain how to write a detailed police incident report for a residential burglary, including the key sections that should be included."
        
        ### 2. Provide Context
        
        **Instead of:** "Summarize this."
        
        **Better:** "I'm reviewing a 3-page witness statement from a traffic accident. Please summarize the key details including what the witness observed, the time and location, and any descriptions of vehicles involved."
        
        ### 3. Specify Format
        
        **Instead of:** "Give me ideas for community outreach."
        
        **Better:** "Provide 5 community outreach program ideas for our police department in a bulleted list. For each idea, include a title, brief description, target audience, and estimated resource requirements."
        
        ## Advanced Prompting Strategies
        
        ### 1. Role Prompting
        
        Frame your prompt by giving the LLM a specific role:
        
        "Act as an experienced detective reviewing a cold case. What questions should I consider asking when re-interviewing witnesses 10 years after the incident?"
        
        ### 2. Step-by-Step Guidance
        
        Ask the LLM to break down complex tasks:
        
        "Walk me through the step-by-step process of documenting evidence at a crime scene, explaining each step in detail."
        
        ### 3. Few-Shot Learning
        
        Provide examples of what you want:
        
        "Here are two examples of clearly written public safety announcements:
        
        Example 1: [example text]
        Example 2: [example text]
        
        Using a similar style and format, write a public safety announcement about preventing package theft during the holiday season."
        
        ## Common Prompting Pitfalls
        
        ### 1. Being Too Vague
        Vague prompts lead to generic, unhelpful responses.
        
        ### 2. Information Overload
        Extremely long, complicated prompts can confuse the model.
        
        ### 3. Assuming Background Knowledge
        The model may not have specific knowledge about your department's procedures or local context.
        
        ### 4. Not Iterating
        Effective prompting often requires refining your approach based on responses.
        
        ## Practical Example: Report Writing Assistant
        
        **Initial prompt:**
        "I need to write a report."
        
        **Improved prompt:**
        "I need to write a detailed incident report about a shoplifting case I responded to. The incident occurred at a convenience store, involving a suspect who concealed merchandise worth approximately $50 and left without paying. The store has video evidence, and there was one witness (the cashier). Help me outline a complete incident report with all necessary sections and key information I should include."
        
        ## Key Takeaways
        
        - Clear, specific prompts yield better results
        - Providing context helps the LLM understand your needs
        - Specifying format and role can guide the LLM's responses
        - Effective prompting is a skill that improves with practice
        """,
        "image_path": "static/images/prompting.png",
        "video_url": "https://www.youtube.com/embed/example4",
        "estimated_time": "20 minutes"
    },
    
    5: {
        "title": "Practical Applications and Responsible Use",
        "description": "Real-world uses of LLMs and ethical considerations.",
        "content": """
        # Practical Applications and Responsible Use
        
        ## Real-World Applications of LLMs
        
        ### General Applications
        
        LLMs can help with a wide range of tasks:
        
        - **Content Creation**: Reports, emails, articles, speeches
        - **Research**: Summarizing information, generating questions, exploring ideas
        - **Learning**: Explaining complex concepts, creating study materials
        - **Problem-Solving**: Breaking down problems, suggesting approaches
        - **Creativity**: Brainstorming ideas, creating stories, generating content
        
        ### Law Enforcement Applications
        
        LLMs can assist in various aspects of law enforcement work:
        
        - **Report Writing**: Drafting, formatting, and proofreading reports
        - **Information Processing**: Summarizing witness statements or case documents
        - **Training Materials**: Creating scenarios, examples, and educational content
        - **Communication**: Crafting public announcements, community messages
        - **Administrative Tasks**: Generating templates, forms, and documentation
        
        ## Practical Examples
        
        ### Example 1: Report Enhancement
        
        **Prompt:**
        "I have a rough draft of an incident report for a traffic accident. Can you help me improve its clarity, ensure it includes all necessary information, and format it professionally? Here's my draft: [insert draft text]"
        
        ### Example 2: Witness Interview Preparation
        
        **Prompt:**
        "I need to interview a witness to a convenience store robbery. Based on the initial information that there was one armed suspect who fled in a vehicle, what are 10 important questions I should ask the witness to gather complete and useful information?"
        
        ### Example 3: Explaining Legal Concepts
        
        **Prompt:**
        "I need to explain 'probable cause' to a new neighborhood watch group without using complex legal jargon. Please help me create a clear, simple explanation with everyday examples they can understand."
        
        ## Responsible and Ethical Use
        
        ### Important Considerations
        
        1. **Privacy and Confidentiality**
           - Never input confidential information, personal data, or sensitive case details
           - Assume anything you type could potentially be saved or accessed
           
        2. **Verification and Accuracy**
           - Always verify LLM-generated information, especially facts, laws, and procedures
           - LLMs can sometimes present incorrect information confidently
           
        3. **Transparency**
           - Be clear when content has been generated or assisted by AI
           - Maintain appropriate human oversight and responsibility
           
        4. **Bias Awareness**
           - Be aware that LLMs can reflect and sometimes amplify societal biases
           - Review outputs for potential bias in language or conclusions
           
        5. **Appropriate Use Cases**
           - Use LLMs for appropriate tasks (drafting, brainstorming, summarizing)
           - Don't rely on LLMs for critical decisions or legal judgments
        
        ## Best Practices for Professional Use
        
        1. **Start simple** - Begin with straightforward tasks as you build experience
        2. **Maintain human review** - Always review and edit AI-generated content
        3. **Use secure, approved tools** - Only use LLMs approved by your organization
        4. **Document AI assistance** - Note when and how AI tools were used
        5. **Continuously learn** - Stay updated on capabilities and limitations
        6. **Provide feedback** - Report problematic outputs to improve systems
        
        ## Key Takeaways
        
        - LLMs offer valuable assistance for many aspects of professional work
        - Appropriate prompting maximizes their utility while minimizing risks
        - Responsible use requires awareness of limitations and ethical considerations
        - Human judgment and oversight remain essential when using AI tools
        """,
        "image_path": "static/images/applications.png",
        "video_url": "https://www.youtube.com/embed/example5",
        "estimated_time": "30 minutes"
    },
    
    6: {
        "title": "AI Ethics and Responsible Use in Law Enforcement",
        "description": "Understanding ethical considerations, biases, and best practices for using AI in law enforcement contexts.",
        "content": """
        # AI Ethics and Responsible Use in Law Enforcement
        
        ## Ethical Considerations in AI for Law Enforcement
        
        As AI becomes more integrated into law enforcement workflows, several important ethical considerations arise:
        
        ### 1. Transparency and Explainability
        
        **Why it matters:** AI systems, especially deep learning models, can be "black boxes" where the decision-making process is not easily explained.
        
        **Best practices:**
        - Prioritize AI tools that provide explanations for their outputs
        - Document how AI tools are used in investigations
        - Be prepared to explain AI-assisted processes in court
        
        ### 2. Fairness and Bias
        
        **Why it matters:** AI systems can perpetuate or amplify existing biases in training data, potentially leading to discriminatory outcomes.
        
        **Best practices:**
        - Be aware that AI systems reflect biases in their training data
        - Use diverse training data when developing AI tools
        - Regularly audit AI systems for biased outputs
        - Never rely solely on AI for decisions that impact people's rights
        
        ### 3. Privacy and Civil Liberties
        
        **Why it matters:** AI can enable more extensive data collection and analysis, potentially infringing on privacy rights.
        
        **Best practices:**
        - Adhere to all relevant privacy laws and regulations
        - Consider whether AI use constitutes a search under the Fourth Amendment
        - Apply the principle of data minimization
        - Use strong data security measures
        
        ## Addressing Bias in AI Systems
        
        ### Types of Bias
        
        - **Data Bias:** When training data doesn't represent the population it will be used on
        - **Algorithm Bias:** When the design of the algorithm itself creates unfair outcomes
        - **Deployment Bias:** When a system is used in contexts it wasn't designed for
        
        ### Strategies for Mitigating Bias
        
        1. **Critical Assessment:** Question what biases might exist in each AI system
        2. **Human Oversight:** Maintain meaningful human review of AI-assisted decisions
        3. **Diverse Input:** Seek feedback from diverse stakeholders on AI implementation
        4. **Regular Testing:** Continuously test systems for biased outcomes
        5. **Training:** Educate personnel on recognizing and addressing AI bias
        
        ## Responsible AI Implementation in Law Enforcement
        
        ### Framework for Responsible AI Use
        
        1. **Need Assessment:** Clearly define the problem you're trying to solve
        2. **Tool Selection:** Choose appropriate tools with known limitations
        3. **Risk Assessment:** Evaluate potential risks before implementation
        4. **Clear Policies:** Develop specific policies governing AI use
        5. **Training:** Ensure all personnel are properly trained
        6. **Auditing:** Regularly review AI system performance
        7. **Community Engagement:** Maintain transparency with the public
        
        ### Case Study: Predictive Policing
        
        Predictive policing tools use historical crime data to predict where crimes might occur or who might commit them.
        
        **Ethical concerns include:**
        - Reinforcing patterns of over-policing in certain communities
        - Creating feedback loops where predictions become self-fulfilling
        - Making decisions based on correlations rather than causation
        
        **Responsible approach:**
        - Use as one of many factors in resource allocation
        - Regularly validate predictions against actual outcomes
        - Be transparent with communities about how the technology is used
        - Combine with community-oriented policing strategies
        
        ## Key Takeaways
        
        - AI tools require careful ethical consideration, especially in law enforcement
        - Transparency, fairness, and privacy should be central concerns
        - Human judgment remains essential—AI should support, not replace human decision-making
        - Regular assessment and auditing of AI systems helps prevent harmful outcomes
        - Community trust depends on responsible AI use and transparency
        """,
        "image_path": "static/images/ai_ethics.png",
        "video_url": "https://www.youtube.com/embed/example6",
        "estimated_time": "25 minutes"
    },
    
    7: {
        "title": "Personal Growth and Productivity with AI",
        "description": "Using AI tools for personal development, learning, and daily tasks.",
        "content": """
        # Personal Growth and Productivity with AI

        ## Personal Development Applications

        ### Learning and Education
        - Using AI to create personalized study plans
        - Getting explanations for complex topics
        - Finding and summarizing educational resources
        - Language learning with AI assistance
        - Creating flashcards and study materials

        ### Career Development
        - Resume and cover letter optimization
        - Interview preparation with AI
        - Skill gap analysis and learning recommendations
        - Professional writing assistance
        - Networking strategy development

        ### Personal Organization
        - Task and schedule management
        - Email organization and response drafting
        - Note-taking and knowledge management
        - Personal finance tracking and analysis
        - Goal setting and progress monitoring

        ## Life Enhancement Applications

        ### Health and Wellness
        - Meal planning and recipe creation
        - Workout routine development
        - Sleep pattern analysis
        - Stress management techniques
        - Mental health resource finding

        ### Home Management
        - Home maintenance scheduling
        - Budget optimization
        - Shopping list generation
        - Home improvement project planning
        - Energy usage optimization

        ### Creative Projects
        - Writing assistance (blogs, stories, poetry)
        - Design idea generation
        - Music and art exploration
        - DIY project planning
        - Creative problem-solving

        ## Practical Examples

        ### Example 1: Personal Learning Plan
        ```
        Prompt: "I want to learn data analysis. Create a 3-month learning plan that fits around a full-time job, breaking down weekly goals and recommended resources."
        ```

        ### Example 2: Career Development
        ```
        Prompt: "Review my resume and suggest improvements to highlight my leadership experience in law enforcement for a private sector security management position."
        ```

        ### Example 3: Life Organization
        ```
        Prompt: "Help me create a monthly budget template that includes savings goals, debt repayment, and discretionary spending categories."
        ```

        ## Best Practices for Personal AI Use

        1. **Start Small**
           - Begin with simple, low-stakes tasks
           - Gradually expand to more complex applications
           - Learn from each interaction

        2. **Maintain Privacy**
           - Never share sensitive personal information
           - Use secure and reputable AI tools
           - Be cautious with financial and health data

        3. **Verify and Validate**
           - Double-check AI suggestions
           - Use AI as a helper, not the final authority
           - Keep human judgment central

        ## Key Takeaways
        - AI can enhance various aspects of personal life
        - Start with basic applications and expand gradually
        - Maintain privacy and security awareness
        - Use AI as a tool for enhancement, not replacement
        """,
        "image_path": "static/images/personal_ai.png",
        "video_url": "https://www.youtube.com/embed/example7",
        "estimated_time": "25 minutes"
    },
    
    8: {
        "title": "Entrepreneurship and Business Applications of AI",
        "description": "Leveraging AI for business creation, growth, and optimization.",
        "content": """
        # Entrepreneurship and Business Applications of AI

        ## Business Creation with AI

        ### Market Research
        - Identifying market opportunities
        - Analyzing competition
        - Understanding customer needs
        - Trend analysis and prediction
        - Demographic research

        ### Business Planning
        - Business plan generation
        - Financial projections
        - Risk assessment
        - Resource planning
        - Marketing strategy development

        ### Product/Service Development
        - Idea validation
        - Feature prioritization
        - Pricing strategy
        - Customer feedback analysis
        - Development roadmap creation

        ## Business Growth Applications

        ### Marketing and Sales
        - Content creation for multiple platforms
        - Social media strategy
        - Email campaign optimization
        - Sales copy writing
        - Customer segmentation

        ### Customer Service
        - Automated response systems
        - Customer inquiry handling
        - FAQ development
        - Feedback analysis
        - Service improvement recommendations

        ### Operations
        - Process optimization
        - Inventory management
        - Scheduling and planning
        - Cost reduction analysis
        - Quality control

        ## Practical Examples

        ### Example 1: Business Idea Validation
        ```
        Prompt: "I'm considering starting a mobile app that helps law enforcement professionals track their continuing education credits. Help me analyze the market potential and create a basic business plan."
        ```

        ### Example 2: Marketing Content
        ```
        Prompt: "Create a month's worth of social media content ideas for a personal security training business, including post types, hashtags, and engagement strategies."
        ```

        ### Example 3: Customer Service
        ```
        Prompt: "Help me develop a customer service response template library for common questions about my online training course platform."
        ```

        ## Implementation Strategy

        1. **Assessment Phase**
           - Identify business needs
           - Evaluate AI tool options
           - Set clear objectives
           - Define success metrics

        2. **Integration Phase**
           - Start with pilot projects
           - Train team members
           - Monitor results
           - Gather feedback

        3. **Optimization Phase**
           - Analyze performance
           - Refine processes
           - Scale successful applications
           - Stay updated on new capabilities

        ## Best Practices for Business AI Use

        1. **Strategic Implementation**
           - Align AI use with business goals
           - Focus on value creation
           - Consider scalability
           - Monitor ROI

        2. **Risk Management**
           - Protect sensitive data
           - Maintain compliance
           - Have backup systems
           - Regular security reviews

        3. **Customer Focus**
           - Enhance customer experience
           - Maintain personal touch
           - Gather and act on feedback
           - Be transparent about AI use

        ## Key Takeaways
        - AI can support various business functions
        - Start with clear objectives and metrics
        - Focus on customer value
        - Maintain security and privacy
        - Scale gradually based on results
        """,
        "image_path": "static/images/business_ai.png",
        "video_url": "https://www.youtube.com/embed/example8",
        "estimated_time": "30 minutes"
    }
}

# Function to get lesson by ID
def get_lesson(lesson_id):
    """Get a specific lesson by ID"""
    return lessons.get(lesson_id, None)

# Function to get all lesson titles
def get_lesson_titles():
    """Get a dictionary of lesson IDs and their titles.
    
    Returns:
        dict: A dictionary mapping lesson IDs to their titles
    """
    return {lesson_id: content["title"] for lesson_id, content in lessons.items()}

# Function to get total number of lessons
def get_lesson_count():
    """Get the total number of available lessons.
    
    Returns:
        int: The number of lessons
    """
    return len(lessons) 