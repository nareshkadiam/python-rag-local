import sys
from openai import OpenAI

def main() -> None:
    with OpenAI() as client:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a short poem about the sea."}
            ],
            max_tokens=100,
            temperature=0.5
        )
        print(response.choices[0].message.content)

def singlecall() -> None:
    with OpenAI() as client:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input="Write a short poem about the sea.",
            max_output_tokens=100,
            temperature=0.5
        )
        print(response.output_text)

# Map command line strings to actual function names
ACTIONS = {
    "singlecall": singlecall
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        # Look up the command in the dictionary and call it safely
        if command in ACTIONS:
            ACTIONS[command]()
        else:
            print(f"Unknown command: '{command}'. Available: {list(ACTIONS.keys())}")
    else:
        main()