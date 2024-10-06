import openai
import streamlit as st

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["api_keys"]["openai_key"]

# Template for formatting the prompt
template = (
    "You are tasked with extracting specific information from the following text content: {website_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_openai(dom_chunks, parse_description):
    # Initialize an empty list to store parsed results
    parsed_results = []

    # Loop through each chunk of website content
    for i, chunk in enumerate(dom_chunks, start=1):
        # Format the system message and user message with the current chunk and description
        formatted_prompt = template.format(website_content=chunk, parse_description=parse_description)

        # Call the OpenAI ChatCompletion model instead of Completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using the chat-based model
            messages=[
                {"role": "system", "content": "You are a helpful assistant for extracting data."},
                {"role": "user", "content": formatted_prompt}
            ]
        )

        # Extract the response content
        parsed_response = response['choices'][0]['message']['content'].strip()
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(parsed_response)

    # Return all parsed results joined by new lines
    return "\n".join(parsed_results)
