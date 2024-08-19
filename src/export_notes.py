import os
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.notestore.NoteStore as NoteStore
from evernote.api.client import EvernoteClient

# Replace with your Evernote developer token
auth_token = "YOUR_DEVELOPER_TOKEN"

# Create a client to connect to Evernote
client = EvernoteClient(token=auth_token, sandbox=False)

# Retrieve the user and note store
user_store = client.get_user_store()
note_store = client.get_note_store()

# Retrieve all notebooks
notebooks = note_store.listNotebooks()

# Create a directory to store the exported notes
output_dir = "Evernote_Export"
os.makedirs(output_dir, exist_ok=True)

# Export all notebooks and their notes
for notebook in notebooks:
    notebook_name = notebook.name
    print(f"Exporting notebook: {notebook_name}")

    # Create a directory for each notebook
    notebook_dir = os.path.join(output_dir, notebook_name)
    os.makedirs(notebook_dir, exist_ok=True)

    # Retrieve all notes in the current notebook
    filter = NoteStore.NoteFilter(notebookGuid=notebook.guid)
    spec = NoteStore.NotesMetadataResultSpec(includeTitle=True)
    note_list = note_store.findNotesMetadata(auth_token, filter, 0, 1000, spec)

    for note_meta in note_list.notes:
        note = note_store.getNote(note_meta.guid, True, True, False, False)

        # Save the note content to a file
        note_title = note.title.replace("/", "-").replace("\\", "-")
        note_filename = os.path.join(notebook_dir, f"{note_title}.html")

        with open(note_filename, "w", encoding="utf-8") as f:
            f.write(note.content)

        print(f"Exported note: {note_title}")

print("Export complete!")

