import os

from prompt_toolkit import prompt
from strands import Agent
from strands.models.openai import OpenAIModel

# 環境変数からAPIキーを取得
api_key = os.environ["OPENAI_API_KEY"]

# モデルを指定してAIエージェントを作成
model = OpenAIModel(
    client_args={
        "api_key": api_key,
    },
    model_id="gpt-4.1",  # 使用するモデルを指定
)
agent = Agent(model=model)

while True:
    # ユーザーからの入力を受け取る
    user_input = prompt("> ")

    # "exit" または "quit" と入力されたら終了
    if user_input.lower() in ["exit", "quit"]:
        break

    # AIエージェントにユーザー入力を渡して応答を出力
    agent(user_input)
    print()
