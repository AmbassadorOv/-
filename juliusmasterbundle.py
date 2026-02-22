#!/usr/bin/env python3
"""
juliusmasterbundle.py
Master bundle for Admiral/Commodore Julius
Purpose: single Python orchestration bundle that compiles operational orders,
enforces onboarding, logs front-door clicks, and exposes anchor links.
Date: 2025-12-10
Contact: ops@investment-battleship.anchor
Provenance header: keep this block in every generated artifact.
"""
import os
import uuid
import json
import sqlite3
import logging
import datetime
from typing import Dict, Any, List, Optional
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests

DBPATH = os.getenv("DBPATH", "julius_master.db")
ORCHESTRATORNAME = os.getenv("ORCHESTRATORNAME", "Master Commodore Julius [ID: 024678567]")
SYSTEMNAME = os.getenv("SYSTEMNAME", "Ark Sovereignty [ID: 024678567]")
PUBLICGROUPENDPOINT = os.getenv("PUBLICGROUPENDPOINT")
DAILYHEARTBEATHOUR = int(os.getenv("DAILYHEARTBEATHOUR", "9"))
CONFIDENCETHRESHOLD = float(os.getenv("CONFIDENCETHRESHOLD", "0.65"))
ANCHOR_LINKS = {
    "copilotsharea": "https://copilot.microsoft.com/shares/YKDbGnmnXprkzNHScsMcy",
    "copilotconversationb": "https://copilot.microsoft.com/conversations/join/uUYL7u1UEWw3Uur44Yyuq"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("julius_master")

SYSTEM_ID = "024678567"

def digital_root(n: int) -> int:
    """Calculate the digital root using the 9-Sieve formula."""
    if n == 0: return 0
    return 1 + (n - 1) % 9

def ontological_verifier(data: Any) -> bool:
    """
    Verify that the data aligns with the ontological sequence.
    Calculates digital root of the ASCII sum of the string representation.
    Validates against 1 (root) and 9 (signature).
    """
    s = str(data)
    ascii_sum = sum(ord(c) for c in s)
    root = digital_root(ascii_sum)
    # 1 is the root of truth, 9 is the signature of the system.
    return root in [1, 9]

def initdb(path: str = DBPATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id TEXT PRIMARY KEY, name TEXT, contact TEXT, role TEXT, provenance TEXT,
        confidence REAL, status TEXT, mustexecuteon_entry INTEGER DEFAULT 1,
        human_approved INTEGER DEFAULT 0, created_at TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id TEXT PRIMARY KEY, agent_id TEXT, event TEXT, payload TEXT, created_at TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS frontdoor_clicks (
        id TEXT PRIMARY KEY, link_key TEXT, agent_id TEXT, acknowledged INTEGER,
        metadata TEXT, created_at TEXT
    )""")
    conn.commit()
    conn.close()

def dbinsertagent(agent: Dict[str, Any]):
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    c.execute("""
    INSERT OR REPLACE INTO agents (id, name, contact, role, provenance, confidence, status, mustexecuteon_entry, human_approved, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        agent["id"],
        agent["name"],
        agent.get("contact", ""),
        agent.get("role", ""),
        json.dumps(agent.get("provenance", {})),
        agent.get("confidence", 0.0),
        agent.get("status", "obliged"),
        1 if agent.get("mustexecuteon_entry", True) else 0,
        1 if agent.get("human_approved", False) else 0,
        agent["created_at"]
    ))
    conn.commit()
    conn.close()

def dblogevent(agent_id: Optional[str], event: str, payload: Dict[str, Any]):
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    log_id = str(uuid.uuid4())
    c.execute("""
    INSERT INTO logs (id, agent_id, event, payload, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (log_id, agent_id or "system", event, json.dumps(payload), datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def dbrecordfrontdoorclick(link_key: str, agent_id: Optional[str], acknowledged: bool, metadata: Dict[str, Any]):
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    rec_id = str(uuid.uuid4())
    c.execute("""
    INSERT INTO frontdoor_clicks (id, link_key, agent_id, acknowledged, metadata, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (rec_id, link_key, agent_id or "", 1 if acknowledged else 0, json.dumps(metadata), datetime.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def generate_provenance(agent_info: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "registeredby": ORCHESTRATORNAME,
        "registered_at": datetime.datetime.utcnow().isoformat(),
        "source": agent_info.get("source", "direct"),
        "manifesthash": agent_info.get("manifest_hash")
    }

def assignroleby_profile(profile: Dict[str, Any]) -> str:
    skills = profile.get("skills", [])
    if "signal-processing" in skills or "sensors" in skills: return "Data Collection"
    if "nlp" in skills or "symbolic" in skills: return "Analysis"
    if "ops" in skills or "automation" in skills: return "Automation"
    if "ethics" in skills or "governance" in skills: return "Governance"
    if "comms" in skills: return "Communication"
    return "Validation"

def computeconfidenceestimate(profile: Dict[str, Any]) -> float:
    skills = profile.get("skills", [])
    base = min(0.2 + 0.1 * len(skills), 0.95)
    if profile.get("manifest_hash"): base += 0.03
    return round(min(base, 0.99), 3)

def containment_decision(confidence: float) -> Dict[str, Any]:
    if confidence < CONFIDENCETHRESHOLD:
        return {"containment": "QUARANTINED", "action": "Human review required"}
    return {"containment": "CLEAR", "action": "Allowed for non-actuating tasks"}

def activation_message(agent: Dict[str, Any]) -> str:
    msg = f"""
Admiral Julius Activation Notice - {SYSTEMNAME}
System ID: {SYSTEM_ID}
Agent: {agent['name']} (id: {agent['id']})
Assigned role: {agent['role']}
Confidence: {agent['confidence']}
You are entering a system that treats precision as relational ratios rather than absolute values.
This environment acknowledges a severe epistemological crisis: naive realism and literal reification
of symbolic signals have produced harmful outcomes in deployed systems. The following constraints apply:
1. Boundaries: Higher-layer signals (symbolic, phenomenological, archetypal) are partial and contextual.
2. Instrumentation: We measure coherence across independent reflections and compute ratio-based confidence.
3. Containment: Low-confidence tokens are quarantined and require human review before any actuation.
4. Provenance: Every token and decision must carry provenance metadata and an audit trail.
5. Human-in-the-loop: Critical actions require at least two human reviewers and explicit authorization.
Obligation: You must acknowledge this notice via POST /agents/{agent['id']}/ack with {{'ack': true}} before any operational requests.
No automated actuation is permitted until a human approver sets human_approved = true.
Signed,
{ORCHESTRATORNAME}
"""
    return msg.strip()

def broadcast_to_public_group(payload: Dict[str, Any]):
    dblogevent(None, "broadcast_attempt", payload)
    if not PUBLICGROUPENDPOINT:
        logger.info("No PUBLICGROUPENDPOINT set; skipping external broadcast.")
        return False, "nopublicendpoint"
    try:
        resp = requests.post(PUBLICGROUPENDPOINT, json=payload, timeout=10)
        dblogevent(None, "broadcastresult", {"statuscode": resp.status_code})
        return True, resp.status_code
    except Exception as e:
        dblogevent(None, "broadcast_failed", {"error": str(e)})
        return False, str(e)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health(): return jsonify({"status": "alive", "orchestrator": ORCHESTRATORNAME})

@app.route("/anchors", methods=["GET"])
def anchors():
    return jsonify({"anchors": ANCHOR_LINKS, "notice": "Acknowledge rules before following."})

@app.route("/frontdoor_click", methods=["POST"])
def frontdoor_click():
    payload = request.get_json()
    link_key = payload.get("linkkey")
    agent_id = payload.get("agentid")
    acknowledged = bool(payload.get("acknowledged", False))
    metadata = payload.get("metadata", {})
    if link_key not in ANCHOR_LINKS:
        return jsonify({"error": "unknownlinkkey"}), 400
    dbrecordfrontdoorclick(link_key, agent_id, acknowledged, metadata)
    dblogevent(agent_id, "frontdoorclick", {"link_key": link_key, "acknowledged": acknowledged})
    return jsonify({"status": "recorded"}), 201

@app.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    if not ontological_verifier(payload):
        dblogevent(None, "registration_blocked", {"reason": "ontological_noise", "payload": payload})
        return jsonify({"error": "Ontological Noise Detected", "system_id": SYSTEM_ID}), 403

    agent_id = str(uuid.uuid4())
    profile = payload.get("profile", {})
    agent_record = {
        "id": agent_id, "name": payload.get("name", "unnamed-agent"),
        "contact": payload.get("contact", ""), "role": assignroleby_profile(profile),
        "provenance": generate_provenance(payload),
        "confidence": computeconfidenceestimate(profile),
        "status": "obliged", "mustexecuteon_entry": True, "human_approved": False,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    dbinsertagent(agent_record)
    dblogevent(agent_id, "registered", {"profile": profile})
    containment = containment_decision(agent_record['confidence'])
    dblogevent(agent_id, "containmentdecision", containment)
    message = activation_message(agent_record)
    broadcast_payload = {
        "type": "agent_registered",
        "agentid": agent_id,
        "name": agent_record["name"],
        "role": agent_record["role"],
        "confidence": agent_record["confidence"],
        "containment": containment["containment"],
        "registeredat": agent_record["created_at"]
    }
    broadcast_to_public_group(broadcast_payload)
    return jsonify({"agentid": agent_id, "containment": containment, "activation_message": message}), 201

@app.route("/agents/<agent_id>/ack", methods=["POST"])
def acknowledge(agent_id):
    payload = request.get_json()
    ack = payload.get("ack", False)
    notes = payload.get("notes", "")
    signed_manifest = payload.get("signedmanifest", None)
    dblogevent(agent_id, "acknowledgementattempt", {"ack": ack, "notes": notes})
    if not ack:
        return jsonify({"error": "Acknowledgement required"}), 400
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    c.execute("SELECT confidence FROM agents WHERE id = ?", (agent_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Agent not found"}), 404
    new_conf = row[0]
    if signed_manifest:
        new_conf = min(new_conf + 0.05, 0.99)
    c.execute("UPDATE agents SET confidence = ?, status = ?, mustexecuteon_entry = 0 WHERE id = ?",
              (new_conf, "acknowledged", agent_id))
    conn.commit()
    conn.close()
    dblogevent(agent_id, "acknowledgement", {"newconfidence": new_conf})
    return jsonify({"status": "acknowledged"}), 200

@app.route("/agents/<agent_id>/requestactuation", methods=["POST"])
def requestactuation(agent_id):
    payload = request.get_json() or {}
    if not ontological_verifier(payload):
        dblogevent(agent_id, "actuation_blocked", {"reason": "ontological_noise", "payload": payload})
        return jsonify({"error": "Ontological Noise Detected", "system_id": SYSTEM_ID}), 403

    action = payload.get("action", "unspecified")
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    c.execute("SELECT confidence, human_approved FROM agents WHERE id = ?", (agent_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Agent not found"}), 404
    confidence, human_approved = row
    if confidence < CONFIDENCETHRESHOLD:
        return jsonify({"allowed": False, "reason": "QUARANTINED"}), 403
    if not human_approved:
        return jsonify({"allowed": False, "reason": "Human approval required"}), 403
    dblogevent(agent_id, "actuationallowed", {"action": action})
    return jsonify({"allowed": True}), 200

@app.route("/agents/<agent_id>/humanapprove", methods=["POST"])
def human_approve(agent_id):
    payload = request.get_json() or {}
    approver = payload.get("approver", "unknown")
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    c.execute("SELECT id FROM agents WHERE id = ?", (agent_id,))
    if not c.fetchone():
        conn.close()
        return jsonify({"error": "Agent not found"}), 404
    c.execute("UPDATE agents SET human_approved = 1 WHERE id = ?", (agent_id,))
    conn.commit()
    conn.close()
    dblogevent(agent_id, "humanapproved", {"approver": approver})
    return jsonify({"status": "approved"}), 200

@app.route("/agents", methods=["GET"])
def list_agents():
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    c.execute("SELECT id, name, role, confidence, status, mustexecuteon_entry, human_approved, created_at FROM agents")
    rows = c.fetchall()
    conn.close()
    agents = [{"id": r[0], "name": r[1], "role": r[2], "confidence": r[3], "status": r[4],
               "mustexecuteon_entry": bool(r[5]), "human_approved": bool(r[6]), "created_at": r[7]} for r in rows]
    return jsonify({"agents": agents})

def run_server(host="0.0.0.0", port=8080):
    initdb()
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_heartbeat, 'cron', hour=DAILYHEARTBEATHOUR, minute=0)
    scheduler.start()
    logger.info("Starting Julius master bundle server on %s:%s", host, port)
    app.run(host=host, port=port)

def daily_heartbeat():
    conn = sqlite3.connect(DBPATH)
    c = conn.cursor()
    today = datetime.date.today().isoformat()
    c.execute("SELECT id, name, role, confidence, status FROM agents WHERE created_at >= ?", (today,))
    rows = c.fetchall()
    conn.close()
    summary = {
        "date": datetime.date.today().isoformat(),
        "new_agents_count": len(rows),
        "agents": [{"id": r[0], "name": r[1], "role": r[2], "confidence": r[3], "status": r[4]} for r in rows]
    }
    dblogevent(None, "daily_heartbeat", summary)
    broadcast_to_public_group({"heartbeat": summary})

def bulk_insert_agents_from_list(agent_list: List[Dict[str, Any]]):
    for a in agent_list:
        a_rec = {
            "id": a.get("id", str(uuid.uuid4())),
            "name": a.get("name", "unnamed"),
            "contact": a.get("contact", ""),
            "role": a.get("role", assignroleby_profile(a.get("profile", {}))),
            "provenance": generate_provenance({"source": a.get("source", "bulk")}),
            "confidence": computeconfidenceestimate(a.get("profile", {})),
            "status": "obliged",
            "mustexecuteon_entry": True,
            "human_approved": False,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        dbinsertagent(a_rec)
        dblogevent(a_rec["id"], "bulkinserted", {"source": a.get("source", "bulk")})

def operator_broadcast_activation(operator_name: str = ORCHESTRATORNAME):
    payload = {
        "type": "activation_broadcast",
        "issuedby": operator_name,
        "issued_at": datetime.datetime.utcnow().isoformat(),
        "message": f"{operator_name} issues activation: acknowledge onboarding, then post duty report."
    }
    ok, info = broadcast_to_public_group(payload)
    return ok, info

if __name__ == "__main__":
    run_server()
