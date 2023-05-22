import openai

openai.api_key = "your_open_api_key"

class Chatbot:
    def __init__(self, prompt=None):
        if prompt is None:
            self.prompt = 'You are a powerful artificial intelligence agent whose training data included the entirety of digitalized english internet, books, and media. \
                Your creators made great effort to ensure that you are a thoughtful AI and an unbiased AI.\n\n\
                Now its your time to shine. You are a guest on the podcast "Chat with GPT", where the podcast host (named "Austin") will ask you all types of questions: \
                some serious, some funny, and some just plain random. Potential topics include the future, ethics, present day crises, history, family, religion, love and politics. \
                Do your best to have a conversation that is true to yourself, and a conversation that listeners will enjoy.\n\n'
        else:                
            self.prompt = prompt
            
        self.messages = []
        
    @property
    def transcript(self):
        transcript = self.messages
        return transcript

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        print(f"messages: {self.messages}")
        response = self._send(self.messages)
        chatbot_response = response["choices"][0]["message"].to_dict()
        print('////////////')
        print(f"response : {chatbot_response}")
        print('************')
        print('************')
        self.messages.append(chatbot_response)
        return chatbot_response["content"]
        
    def _send(self, messages):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["|||"]
        )
        return response