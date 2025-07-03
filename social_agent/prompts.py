# prompts.py

def content_generation_prompt(user_message: str, research_content: str, platform: str) -> str:
    return f"""
    Generate 5 posts for social media platform {platform} for the topic: {user_message}.
    You can use the following researched content:
    {research_content}

    End each post with the marker [[END]].
    Only return the ideas – do not add any introduction or explanation.
    """.strip()


def revise_content_prompt(human_message: str, original_content: str, feedback: str) -> str:
    return f"""
    The user wants to create a social media post about: {human_message}.
    Here are the original ideas: {original_content}
    Please revise them according to this feedback: {feedback}

    End each revised idea with [[END]].
    Return only the revised ideas.
    """.strip()


def should_research_prompt(user_message: str) -> str:
    return f"""
    A user wants to write a social media post about the following topic:
    
    "{user_message}"
    
    Should the system perform external research before generating content?
    Respond with only "yes" or "no".
    """.strip()
