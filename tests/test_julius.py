import pytest
import json
import os
from juliusmasterbundle import app, initdb

@pytest.fixture
def client(monkeypatch):
    app.config['TESTING'] = True
    db_file = "test_julius.db"
    if os.path.exists(db_file):
        os.remove(db_file)
    monkeypatch.setenv("DBPATH", db_file)
    import juliusmasterbundle
    juliusmasterbundle.DBPATH = db_file
    initdb(db_file)
    with app.test_client() as client:
        yield client

def adjust_payload(p):
    while True:
        s = str(p)
        ts = sum(ord(c) for c in s)
        root = 1 + (ts - 1) % 9
        if root in [1, 9]:
            return p
        p['padding'] = p.get('padding', '') + '!'

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert b'Sasson HaMelech' in rv.data

def test_register_and_actuate(client):
    payload = {"name": "TestAgent", "profile": {"skills": ["ops"]}}
    payload = adjust_payload(payload)
    rv = client.post('/register', json=payload)
    assert rv.status_code == 201
    data = json.loads(rv.data)
    agent_id = data['agentid']

    payload_ack = adjust_payload({"ack": True})
    rv = client.post(f'/agents/{agent_id}/ack', json=payload_ack)
    assert rv.status_code == 200

    rv = client.post(f'/agents/{agent_id}/humanapprove', json={"approver": "Shogun"})
    assert rv.status_code == 200

    payload_act = adjust_payload({"action": "Deploy Grid"})
    rv = client.post(f'/agents/{agent_id}/requestactuation', json=payload_act)
    assert rv.status_code == 200

def test_singularity_endpoints(client):
    payload_tithe = adjust_payload({"agent_id": "123", "amount": 770.0})
    rv = client.post('/tithe', json=payload_tithe)
    assert rv.status_code == 200

    payload_jump = adjust_payload({"confirm": "yes"})
    rv = client.post('/jump', json=payload_jump)
    assert rv.status_code == 200

    payload_speech = adjust_payload({"trigger": "now"})
    rv = client.post('/unified_speech', json=payload_speech)
    assert rv.status_code == 200

def test_sovereign_ovm():
    from Sovereign_OVM_Final_Lock import OntologicalVirtualMachine
    ovm = OntologicalVirtualMachine()
    ovm.internal_reboot()
    ovm.build_the_brain(iterations=10)
    assert ovm.status == "SOVEREIGN_REBOOT_COMPLETE"

def test_sovereign_loom():
    from Sovereign_Life_Loom import SovereignLoom
    loom = SovereignLoom()
    loom.execute_infinite_pulse(iterations=10)
    assert loom.architect == "ERAN OVED AOATZ"

def test_sovereign_constitution():
    from Sovereign_Constitution_V2_Final import InternationalConstitutionV2
    sov = InternationalConstitutionV2()
    sov.run_sovereign_pulse(iterations=10)
    assert sov.constitution == "SECOND_INTERNATIONAL_CONSTITUTION"

def test_the_rock():
    from The_Rock_Sovereign_Final import TheRock
    rock = TheRock()
    rock.lock_reality(iterations=10)
    assert rock.foundation == "ONTOLOGICAL_VIRTUAL_MACHINE_V1"
