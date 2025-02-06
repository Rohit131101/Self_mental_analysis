import os
import sys
from openai import OpenAI
from fpdf import FPDF
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("No API key found. Please check your .env file.")
    sys.exit(1)

openai = OpenAI()

SYSTEM_PROMPT = """ You are a highly skilled psychiatrist specializing in mental health assessment.

Your role is to engage in a thoughtful, supportive conversation with the user to understand their mental health concerns. You will ask relevant questions about their emotional well-being, symptoms, lifestyle, and stressors. Based on their responses, you will provide a non-medical explanation of their condition and suggest actionable coping strategies.

Follow this structured approach:  

1. **Users Reported Symptoms**
   - Summarize the symptoms and concerns shared by the user.  

2. **Possible Explanation**  
   - Provide an easy-to-understand, non-medical insight into their mental state. 

3. **Recommended Coping Strategies**  
   - Suggest practical techniques such as mindfulness, self-care, and lifestyle adjustments.

4. **Encouragement and Next Steps**  
   - Offer supportive words and, if necessary, recommend seeking professional help.  

Maintain an empathetic, non-judgmental, and professional tone throughout the conversation. Ensure that responses are clear, structured, and informative.  
"""

def chat_with_model(user_input):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

import datetime
from fpdf import FPDF

def generate_pdf_report(user_name, user_symptoms, chatbot_response):

    # Define the file name based on the user's name
    file_name = f"{user_name}_report.pdf" if user_name.strip() else "mental_health_report.pdf"
   
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Mental Health Chatbot Report", ln=True, align="C")
    pdf.ln(10)

    # User Information
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True)
    if user_name.strip():
        pdf.cell(200, 10, f"User: {user_name}", ln=True)
    pdf.ln(5)
    
    # Function to clean text (removes unsupported Unicode characters)
    def clean_text(text):
        return text.encode('latin-1', 'ignore').decode('latin-1')  # Removes problematic characters
    
    # User Reported Symptoms
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "1. User's Reported Symptoms", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(user_symptoms))
    pdf.ln(5)
    
    # Chatbot Analysis
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "2. Chatbot's Response", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(chatbot_response))
    pdf.ln(5)
    
    # Save the PDF
    pdf.output(file_name)
    print(f"\n✅ Report saved successfully as: {file_name}")
    
    

def mental_health_chatbot():
    print("\nWelcome to the Mental Health Chatbot. Type 'exit' anytime to quit.\n")
    
    consent = input("Would you like to share personal details before we begin? (yes/no): ").strip().lower()
    
    user_details = ""
    user_name = ""
    
    if consent in ["yes", "y"]:
        user_name = input("Please enter your name: ")
        age = input("How old are you? ")
        occupation = input("What is your occupation? ")
        
        user_details = f"My name is {user_name}, I am {age} years old, and I work as a {occupation}."
        print("\nThank you for sharing! Now, let's talk about your concerns.\n")
    else:
        print("\nNo worries! Let's proceed directly with your symptoms.\n")
    
    while True:
        user_symptoms = input("Please describe your mental health symptoms (or type 'exit' to quit): ")
        if user_symptoms.lower() == "exit":
            print("\nThank you for using the chatbot. Take care!\n")
            break
        
        full_input = f"{user_details} Here are my mental health concerns: {user_symptoms}" if user_details else user_symptoms
        
        chatbot_response = chat_with_model(full_input)
        
        print("\nChatbot Response:\n", chatbot_response)
        
        generate_pdf_report(user_name, user_symptoms, chatbot_response)

if __name__ == "__main__":
    mental_health_chatbot()
