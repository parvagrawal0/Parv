from uvicorn.middleware.wsgi import WSGIMiddleware

from app import create_app

# Expose an ASGI `app` so you can run:
#   uvicorn main:app --reload
app = WSGIMiddleware(create_app())

