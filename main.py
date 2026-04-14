from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World!"}

@app.get("/api/posts")
def get_posts():
    with open("snippets.txt", "r") as file:
        data = file.read()
    return data

# print(get_posts())
