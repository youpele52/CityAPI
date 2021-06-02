#  entry point for running the app
import uvicorn


if __name__ == "__main__":
    # default port for fastapi is 8000
    # reload here means the debug mode, set to true in development and false in production/when you deploy app
    uvicorn.run("app.app:app", host="127.0.0.1", port=8000, reload=True)
