import os

from mcp import StdioServerParameters, stdio_client
from prompt_toolkit import prompt
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

# 環境変数からAPIキーを取得
api_key = os.environ["OPENAI_API_KEY"]

# モデルを指定してAIエージェントを作成
model = OpenAIModel(
    client_args={
        "api_key": api_key,
    },
    model_id="gpt-4.1",  # 使用するモデルを指定
)

# Fetch MCP Serverのクライアントを作成
fetch_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "mcp/fetch"],
        )
    )
)

# Sequential Thinking MCP Serverのクライアントを作成
seq_think_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "mcp/sequentialthinking"],
        )
    )
)

# Time MCP Serverのクライアントを作成
time_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "mcp/time"],
        )
    )
)

with fetch_mcp_client, seq_think_mcp_client, time_mcp_client:
    # MCPサーバーからツールを取得
    tools = (
        fetch_mcp_client.list_tools_sync()
        + seq_think_mcp_client.list_tools_sync()
        + time_mcp_client.list_tools_sync()
    )

    # モデルとツールを指定してAIエージェントを作成
    agent = Agent(model=model, tools=tools)

    while True:
        # ユーザーからの入力を受け取る
        user_input = prompt("> ")

        # "exit" または "quit" と入力されたら終了
        if user_input.lower() in ["exit", "quit"]:
            break

        # AIエージェントにユーザー入力を渡して応答を出力
        agent(user_input)
        print()
