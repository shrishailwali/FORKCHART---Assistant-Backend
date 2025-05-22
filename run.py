from app.main import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", reload=True)