from fastapi import FastAPI, HTTPException, status

app = FastAPI()

notes = []

@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/notes")
def get_notes():
    return notes


@app.get("/notes/{id}")
def get_note(id: int):
    for note in notes:
        if note["id"] == id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.post("/notes", status_code= status.HTTP_201_CREATED)
def create_note(note: dict):
    note["id"] = len(notes) + 1
    notes.append(note)
    return note


@app.put("/notes/{id}")
def update_note(id: int, updated_note: dict):
    for note in notes:
        if note["id"] == id:
            note["title"] = updated_note["title"]
            note["content"] = updated_note["content"]
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int):
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            return
    raise HTTPException(status_code=404, detail="Note not found")