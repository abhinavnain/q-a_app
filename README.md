<h1 align="center">
  Question & Answer App
</h1>

## Description
The application demonstrates a very simple 5 Step RAG Pattern described in - https://python.langchain.com/docs/use_cases/question_answering/
1. Load
2. Split
3. Store
4. Retrieve
5. Generate
...
## Request Format
```shell
{
    "file_path": "https://remote-path.to/some-file.json",
    "questions": [
        "What is my name?",
        "What is your name? Tell me, please senpai!",
        "Is it cloudy with a chance of meatballs?"
    ]
}
```

<h3>The app then recieves the request, loads the file and pushes it as OpenAI Embeddings for Question and Answering</h3>

## Response Format
```shell
[
    {
        "What is my name?": "I dont know your name."
    },
    {
        "What is your name? Tell me, please senpai!": "My Name is Heisenberg"
    },
    {
        "Is it cloudy with a chance of meatballs?": "Based on my calculations there is a 3.14% chance of pie."
    }
]
```

## Pre-Requisites - Environment Variables
OPENAI_API_KEY - OpenAI API Key from your OpenAI Account
