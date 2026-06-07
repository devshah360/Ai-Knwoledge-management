from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
        response = client.post("/auth/login",json={"username":"example@gmail.com","password":"passowrd"})

        assert response.status_code == 200

def test_document_upload():
        pass

def test_hybrid_search():
        response = client.get("/search?q=fastapi")
        assert response.status_code == 200

def test_chat():
        response = client.post("/chat",json={"question":"What is Fastapi"})

        assert response.status_code == 200

def test_dashboard():
        
        response = client.get("/dashboard/summary")
        
        assert response.status_code == 200

def test_migration():
        response = client.post("/migration/start")

        assert response.status_code == 200


def test_agents():
        pass