import os

import sentry_sdk
from flask import Flask

# 環境変数からSentryのDSNを取得
sentry_dsn = os.environ["SENTRY_DSN"]

# Sentry SDKの初期化
sentry_sdk.init(
    dsn=sentry_dsn,
    send_default_pii=True,
)

app = Flask(__name__)


@app.route("/")
def hello_world():
    # ゼロ除算で例外を発生させる
    1 / 0
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=True)
