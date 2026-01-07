#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_prompt(prompt_type):
    prompts = {
        "greeting": "Hello! Welcome to TalentScout Hiring Assistant. Let's start with your Full Name:"
    }
    return prompts.get(prompt_type, "")

if __name__ == "__main__":
    print("Function defined successfully")
    print(get_prompt("greeting"))