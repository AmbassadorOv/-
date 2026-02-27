import pytest
import json
import sqlite3
import os
import juliusmasterbundle
from juliusmasterbundle import app, initdb

@pytest.fixture
def client():
    # Setup temporary database
    test_db = "test_julius.db"
    os.environ["DBPATH"] = test_db
    juliusmasterbundle.DBPATH = test_db
    initdb(test_db)

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

    # Teardown
    if os.path.exists(test_db):
        os.remove(test_db)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "alive"
    assert "Sasson HaMelech" in data["orchestrator"]

def test_anchors(client):
    response = client.get("/anchors")
    assert response.status_code == 200
    data = response.get_json()
    assert "anchors" in data
    assert "copilotsharea" in data["anchors"]

def test_agent_lifecycle(client):
    # 1. Register
    reg_payload = {
        "name": "Test Agent",
        "profile": {"skills": ["nlp", "symbolic", "ops", "automation", "ethics"]}
    }
    response = client.post("/register", json=reg_payload)
    assert response.status_code == 201
    reg_data = response.get_json()
    agent_id = reg_data["agentid"]
    assert agent_id is not None

    # 2. Acknowledge
    ack_payload = {"ack": True, "notes": "Accepting protocols"}
    response = client.post(f"/agents/{agent_id}/ack", json=ack_payload)
    assert response.status_code == 200

    # 3. Request actuation (should fail without human approval)
    response = client.post(f"/agents/{agent_id}/requestactuation", json={"action": "test"})
    assert response.status_code == 403

    # 4. Human Approve
    response = client.post(f"/agents/{agent_id}/humanapprove", json={"approver": "Admin"})
    assert response.status_code == 200

    # 5. Request actuation (should now succeed)
    response = client.post(f"/agents/{agent_id}/requestactuation", json={"action": "test"})
    assert response.status_code == 200
    assert response.get_json()["allowed"] is True

def test_list_agents(client):
    client.post("/register", json={"name": "A1", "profile": {}})
    client.post("/register", json={"name": "A2", "profile": {}})
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["agents"]) >= 2

def test_tithe(client):
    payload = {"agent_id": "test-agent", "amount": 0.5}
    response = client.post("/tithe", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "tithe_accepted"
    assert data["amount"] == 0.5

def test_jump(client):
    payload = {"target": "8th_Aeon"}
    response = client.post("/jump", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "jump_sequenced"
    assert data["target"] == "8th_Aeon"

def test_unified_speech(client):
    response = client.get("/unified_speech")
    assert response.status_code == 200
    data = response.get_json()
    assert "unified_speech" in data
    assert data["unified_speech"]["EMET-KAYAM"] == "Absolute Truth"

def test_error_handling_malformed_json(client):
    # Test with malformed JSON string
    response = client.post("/register", data="not a json", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "malformed_json"

def test_error_handling_missing_keys(client):
    # Missing 'profile' in /register
    response = client.post("/register", json={"name": "NoProfile"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "missing_profile"

    # Missing 'linkkey' in /frontdoor_click
    response = client.post("/frontdoor_click", json={"agentid": "123"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "missing_linkkey"
