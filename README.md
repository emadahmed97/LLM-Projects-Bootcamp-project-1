# How to run this project / Use it

Run `docker-compose up`
- This will take a while on initial run
- It is finished running when you see `INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`
- You will want to navigate to http://localhost:8501/ which is where the streamlit app is running
- You can search and should see the top 4 results

# How it works
- Uses docker-compose to start 3 services: backend (FastAPI), frontend (streamlit) and db (postgres)
- The backend parses through the `/files` folder and iterates through each file, creates the embeddings and stores in postgres and the faiss index
- When you search, we create the embeddings from the search, perform a faiss search and then get the text from sql. This is then shown in the UI via streamlit
- The main file is `main.py`
