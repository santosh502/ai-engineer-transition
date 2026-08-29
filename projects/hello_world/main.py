import ollama


def hello_world():
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "say hellow world in creative way"
            }
        ]
    )
    print(response['message']['content'], end="\n")
    print("Hello, World!")


def hello_world_stream():
    stream = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "say hellow world in creative way"
            }
        ],
        stream=True
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)


if __name__== "__main__":
    hello_world()

    hello_world_stream()