import json

def test_get_episodes(client, sample_data):
    """Test GET /episodes"""
    response = client.get('/episodes')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data) == 2
    assert 'date' in data[0]

def test_get_episode_by_id(client, sample_data):
    """Test GET /episodes/<id>"""
    response = client.get('/episodes/1')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['id'] == 1
    assert 'appearances' in data
    assert len(data['appearances']) > 0

def test_get_episode_not_found(client):
    """Test GET /episodes/<id> with invalid id"""
    response = client.get('/episodes/999')
    
    assert response.status_code == 404

def test_delete_episode(client, sample_data):
    """Test DELETE /episodes/<id>"""
    response = client.delete('/episodes/1')
    
    assert response.status_code == 204
    
    # Verify deleted
    response = client.get('/episodes/1')
    assert response.status_code == 404

def test_delete_episode_not_found(client):
    """Test DELETE /episodes/<id> with invalid id"""
    response = client.delete('/episodes/999')
    
    assert response.status_code == 404

def test_get_guests(client, sample_data):
    """Test GET /guests"""
    response = client.get('/guests')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data) == 2
    assert 'name' in data[0]

def test_create_appearance_success(client, sample_data):
    """Test POST /appearances with valid data"""
    payload = {
        'rating': 5,
        'episode_id': 1,
        'guest_id': 1
    }
    
    response = client.post('/appearances',
                          data=json.dumps(payload),
                          content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['rating'] == 5
    assert 'episode' in data
    assert 'guest' in data

def test_create_appearance_missing_fields(client, sample_data):
    """Test POST /appearances with missing fields"""
    payload = {'rating': 5}
    
    response = client.post('/appearances',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_create_appearance_invalid_episode(client, sample_data):
    """Test POST /appearances with invalid episode_id"""
    payload = {
        'rating': 5,
        'episode_id': 999,
        'guest_id': 1
    }
    
    response = client.post('/appearances',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_create_appearance_invalid_rating(client, sample_data):
    """Test POST /appearances with invalid rating"""
    payload = {
        'rating': 10,
        'episode_id': 1,
        'guest_id': 1
    }
    
    response = client.post('/appearances',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400