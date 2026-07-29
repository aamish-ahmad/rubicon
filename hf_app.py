"""Hugging Face Space entrypoint.

Keeps the existing API and /ui route while also serving the Gradio interface
at the Space root so it renders inside the Hugging Face embedded viewer.
"""

import gradio as gr

from app import api, demo


# The original app defines a redirect from `/` to `/ui`. Remove only that
# redirect, then mount the same Gradio UI at `/`. Existing API endpoints and
# the legacy `/ui` mount remain available.
api.router.routes = [
    route
    for route in api.router.routes
    if not (
        getattr(route, "path", None) == "/"
        and "GET" in (getattr(route, "methods", None) or set())
    )
]

app = gr.mount_gradio_app(api, demo, path="/")
