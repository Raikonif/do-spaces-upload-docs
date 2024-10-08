import os

import authsignal.client

authsignal_client = authsignal.Client(
    api_key=os.getenv('AUTH_SIGNAL_SECRET_KEY'),
    api_url=os.getenv('AUTH_SIGNAL_BASE_URL')
)
