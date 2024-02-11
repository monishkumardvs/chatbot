import spacy
import wikipedia

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Define responses for different intents
responses = {
    'greeting': ["Hello!", "Hi there!", "Hey! How can I assist you?"],
    'weather': ["I'm sorry, I can't check the weather right now."],
    'goodbye': ["Goodbye!", "See you later!", "Have a great day!"]
}

def process_input(user_input):
    """Process user input and classify intent using spaCy."""
    doc = nlp(user_input.lower())
    intent = None
    for token in doc:
        if token.text in ['hi', 'hello', 'hey']:
            intent = 'greeting'
        elif token.text in ['weather', 'temperature']:
            intent = 'weather'
        elif token.text in ['bye', 'goodbye']:
            intent = 'goodbye'
        elif token.text in ['search', 'find'] and token.head.text == 'Wikipedia':
            intent = 'wikipedia_search'
    return intent

def chatbot_response(user_input, context=None):
    """Generate response based on user input and context."""
    intent = process_input(user_input)
    if intent == 'wikipedia_search':
        query = user_input.split('Wikipedia')[-1].strip()
        try:
            summary = wikipedia.summary(query)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return "Sorry, I found multiple results. Can you please provide more details?"
        except wikipedia.exceptions.PageError as e:
            return "Sorry, I could not find information on that topic."
        except Exception as e:
            return "Sorry, I encountered an issue while processing the Wikipedia response. Please try again later."
    elif intent:
        return responses[intent][0]  # Return first response for simplicity
    else:
        return "Sorry, I didn't understand that."

# Main loop for conversation
def main():
    print("Chatbot: Hello! I'm a smart chatbot. How can I assist you today?")
    context = None  # Initialize context
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input, context)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
