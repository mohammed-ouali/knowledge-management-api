## Knowledge Management API — concise architecture

This file shows a compact Mermaid visualization of the project's layers and database relationships.

### High-level architecture

```mermaid
flowchart TB

    Client["Client / Frontend"]

    API["FastAPI app<br/>(app/main.py)"]

    subgraph Routes["API Routers"]
        Users["/users"]
        Folders["/folders"]
        Notes["/notes"]
    end

    subgraph Services["Business Logic"]
        UserSvc["UserService"]
        FolderSvc["FolderService"]
        NoteSvc["NoteService"]
        LabelSvc["LabelService"]
    end

    subgraph Repos["Persistence"]
        UserRepo["UserRepository"]
        FolderRepo["FolderRepository"]
        NoteRepo["NoteRepository"]
        LabelRepo["LabelRepository"]
    end

    DB["Async SQLAlchemy<br/>Base + SessionLocal + get_db"]

    Client --> API
    API --> Routes
    Routes --> Services
    Services --> Repos
    Repos --> DB
```


### Data model relationships

```mermaid
erDiagram
  USER ||--o{ FOLDER : "owns"
  USER ||--o{ NOTE : "creates"
  FOLDER ||--o{ FOLDER : "parent/subfolders"
  FOLDER ||--o{ NOTE : "contains"
  NOTE ||--o{ LABEL : "has"

  USER {
    int id
    string username
    string email
  }

  FOLDER {
    int id
    int user_id
    int parent_id
    string name
  }

  NOTE {
    int id
    int user_id
    int folder_id
    string title
  }

  LABEL {
    int id
    int note_id
    string name
  }
```

### Typical request flow

```mermaid
sequenceDiagram
  Client->>API: HTTP request (e.g. GET /api/v1/notes)
  API->>Routes: matched router (notes)
  Routes->>Services: call business logic (NoteService)
  Services->>Repos: fetch/persist via repositories
  Repos->>DB: SQLAlchemy async session queries
  DB-->>Repos: results
  Repos-->>Services: domain models
  Services-->>Routes: response schemas
  Routes-->>Client: JSON response
```

### Where to look in the code

- app/main.py: FastAPI entrypoint and middleware
- app/api/v1/router.py and app/api/v1/routers/*: endpoints
- app/services/*: application business rules
- app/repositories/*: database access
- app/models/*: SQLAlchemy models and relationships
- app/core/*: config, database, exceptions

If you'd like a presentation-ready version or a narrower focus (only DB ERD or only request flows), tell me which and I'll produce it.
