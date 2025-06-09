"""Super simple tests to get you started!"""

def test_app_works(client):
    """Test that your app is working"""
    response = client.get("/")
    assert response.status_code == 200
    
def test_health_check(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_nonexistent_page(client):
    """Test that wrong URLs give 404"""
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404