import anthropic
client = anthropic.Anthropic()
response = client.messages.create(model='claude-haiku-4-5-20251001',
                       max_tokens=200,
                       messages=[
                           {'role': 'user', 'content':'In one sentence, what is NIST SP 800-53?'}
                        ]
                    )
print(response.content[0].text)