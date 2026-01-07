def generate_technical_questions(tech_stack):
    techs = [t.strip() for t in tech_stack.split(",")]

    questions = []
    for tech in techs:
        questions.append(f"What are the core concepts of {tech}?")
        questions.append(f"Explain a real-world project where you used {tech}.")
        questions.append(f"What challenges have you faced while working with {tech}?")

    return questions[:5]
