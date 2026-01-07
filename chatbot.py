from prompts import get_prompt
from tech_questions import generate_technical_questions
from data_handler import store_candidate_data

FIELDS = [
    "Full Name",
    "Email Address",
    "Phone Number",
    "Years of Experience",
    "Desired Position(s)",
    "Current Location",
    "Tech Stack"
]

def get_bot_response(user_input, state):
    if "step" not in state:
        state["step"] = 0
        return get_prompt("greeting")

    step = state["step"]

    if step < len(FIELDS):
        field = FIELDS[step]
        store_candidate_data(state, field, user_input)
        state["step"] += 1

        if state["step"] < len(FIELDS):
            return f"Please enter your **{FIELDS[state['step']]}**:"
        else:
            tech_stack = state.get("Tech Stack", "")
            if tech_stack:
                questions = generate_technical_questions(tech_stack)
                q_text = "\n".join([f"• {q}" for q in questions])
                return (
                    "Thank you! 🙌 Based on your tech stack, here are some technical questions:\n\n"
                    f"{q_text}\n\n"
                    "This concludes the screening. Our team will contact you soon."
                )
            else:
                return "Thank you for providing your information! Our team will contact you soon."
    
    return "Thank you for your response!"
