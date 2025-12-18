from openai import OpenAI

client = OpenAI(
    api_key="sk-vzAMTxwXvQK3psfj4879FcEaEa0049808e04322362F2B4C8",
    base_url="https://api.laozhang.ai/v1"
)

models = client.models.list()

print("\nAvailable models from LaoZhang:\n")
for m in models.data:
    print("-", m.id)
