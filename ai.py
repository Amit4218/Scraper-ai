from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {website_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the Ollama model
model = Ollama(model="llama3.2")

def parse_with_ollama(dom_chunks, parse_description):
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize an empty list to store parsed results
    parsed_results = []

    # Loop through each chunk of website content
    for i, chunk in enumerate(dom_chunks, start=1):
        # Format the prompt with the current chunk and description
        formatted_prompt = prompt.format(website_content=chunk, parse_description=parse_description)
        
        # Call the model to process the prompt
        response = model.invoke(formatted_prompt)
        
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    # Return all parsed results joined by new lines
    return "\n".join(parsed_results)