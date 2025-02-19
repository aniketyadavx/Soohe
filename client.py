from openai import OpenAI
client = OpenAI(
api_key = "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",

)



completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Soohee skilled in general task like Alexa and Google cloud"},
        {
            "role": "user",
            "content": "What is Coding."
        }
    ]
)

print(completion.choices[0].message.content)