import openai

openai.api_key = "<DeepSeek API Key>"
openai.base_url = "https://api.deepseek.com/v1"

response = openai.ChatCompletion.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
)

print(response['choices'][0]['message']['content'])
