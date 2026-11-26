# Tutorial

## Step 1: Move PDFs into data with category subfolders 
```
data
|_PDFs
  |_Caisses
  |_Palettes
  |_Pallox
  |_Poubelles
  |_Scelle
```

## Step 2: Create PostgreSQL database to save your data
1. Create docker-compose.yml
```
services:
    postgres:
        image: pgvector/pgvector:pg17 # Name of the image
        container_name: specmind-db
        restart: unless_stopped # Optional
    
    environment:
        POSTGRES_USER: specmind
        POSTGRES_PASSWORD: specmind_dev
        POSTGRES_DB: specmind
    
    ports:
        - "127.0.0.1:5433.5432"
    volumes:
        - postgres_data:/var/lib/postgresql/data

volumes:
    postgres_data

```