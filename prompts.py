def get_prompt(prompt_type):
    prompts = {
        "greeting": (
            "Hello! 👋 Welcome to TalentScout Hiring Assistant.\n\n"
            "I will collect some basic information and then ask technical questions.\n\n"
            "Let's start with your **Full Name**:"
        )
    }
    return prompts.get(prompt_type, "")