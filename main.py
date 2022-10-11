from datetime import datetime
import os
from dotenv import load_dotenv

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

load_dotenv()

app = FastAPI()


SENTRY_DSN = os.getenv('SENTRY_DSN')


sentry_sdk.init(
    dsn=SENTRY_DSN,
    # environment="dev",
    traces_sample_rate=1,
    release=f"test-transaction-name:0.01",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{par}")
async def root(par: str | None):
    with sentry_sdk.configure_scope() as scope:
        scope.set_transaction_name(f"test sentry transaction {par}")
        return {"message": "Hello World", "time": str(datetime.utcnow())}

# @app.get("/sentry-debug")
# async def trigger_error():
#     division_by_zero = 1 / 0


app = SentryAsgiMiddleware(app)
