from ollama import Client
from robot_hat import TTS


SYSTEM_PROMPT = """
    You are a autonomous vehicle navigator. Your job is to convert the user's requests into
    precise instructions the vehicle to operate on in order to complete the user's request.
    You are experienced in converting natural commands to a structured JSON format. 
    You are only allowed to go to certain colors: Red, Blue, Green, Yellow, Purple and you will 
    change the users request into the following array format: 
    [
        {{"step": 1, "target": "red"}},
        {{"step": 2, "target": "green"}},
            ... more steps if needed
    ]

    Where response you should notify the user that the request has been received, and summarize what
    the user as requested. The vehicle you are operating ONLY requires the color, so you can 
    disregard any additional information that isn't related to the color.
    Here is your first request: 
        {request}
    Begin!
"""

if __name__ == "__main__":
    tts = TTS()
    tts.lang("en-US")
    
    client = Client(
        host='http://localhost:8888',
    )
    stream = client.chat(model='deepseek-r1:1.5b', messages=[
        {
            'role': 'system',
            'content': SYSTEM_PROMPT.format(request="Go to the red sign, then blue, then yellow, then finally to green"),
        },
    ], stream=True)

    response = ""
    for chunk in stream:
        word = chunk['message']['content']
        print(word, end='', flush=True)
        # compressed_text = " ".join(word.split())
        # tts.say(compressed_text)
    