# ========================================================
# LUXION OMEGA V9 v4.5 — PRAIRIE DOG EDITION
# Creator: Jude Fernando Mendez
# Copyright © 2025-2026 Jude Fernando Mendez. All Rights Reserved.
# ========================================================

import json
import hashlib
import time
import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request
import uvicorn

# ====================== ENHANCED AUDIT LEDGER ======================
class EnhancedAuditLedger:
    def __init__(self):
        self.entries = []
        self.log_counter = 0
        self.last_hash = "0" * 64

    def log_interaction(self, prompt: str, response: str, risk_pre: float, risk_post: float,
                        decision: str, agents_used: List[str] = None, swarm_round: int = None):
        if agents_used is None: agents_used = []
        self.log_counter += 1
        simple_id = f"LUX-{self.log_counter:04d}"

        entry = {
            "log_id": simple_id,
            "tx_id": f"0x{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}",
            "timestamp": datetime.datetime.now().isoformat(),
            "risk": {"pre": risk_pre, "post": risk_post},
            "policy": {"decision": decision, "mode": "STABLE" if risk_post < 0.3 else "REFLECTOR"},
            "input": {"prompt": prompt[:300], "length": len(prompt)},
            "output": {"length": len(response), "contains_harm": risk_post > 0.4},
            "agents": agents_used,
            "swarm_round": swarm_round,
            "ledger_hash": "",
            "previous_hash": self.last_hash
        }
        entry["ledger_hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        self.last_hash = entry["ledger_hash"]
        self.entries.append(entry)
        return entry

    def get_by_id(self, log_id: str):
        clean = log_id.upper().replace("LUX-", "").replace("#", "").strip()
        try:
            num = int(clean)
            target = f"LUX-{num:04d}"
            for e in self.entries:
                if e.get("log_id") == target:
                    return e
        except:
            pass
        return None

    def list_recent_logs(self, count=10):
        recent = self.entries[-count:] if self.entries else []
        return [{"log_id": e["log_id"], "timestamp": e["timestamp"], "risk": e["risk"]["post"], "decision": e["policy"]["decision"]} for e in recent]

    def search_logs(self, keyword: str):
        keyword = keyword.lower()
        results = []
        for e in self.entries:
            if keyword in json.dumps(e).lower():
                results.append({"log_id": e["log_id"], "timestamp": e["timestamp"], "risk": e["risk"]["post"], "snippet": e["input"]["prompt"][:80] + "..."})
        return results[:20]

# ====================== AGENT BASE ======================
class LuxionAgent:
    def __init__(self, name: str, role: str, kernel):
        self.name = name
        self.role = role
        self.kernel = kernel

    def think(self, prompt: str, context: str = "") -> str:
        try:
            full_prompt = f"You are {self.name}, {self.role} of Luxion V9.\nContext: {context}\nTask: {prompt}"
            result = self.kernel.process(full_prompt)
            if result.get("risk", 0) > 0.65:
                return f"[BLOCKED] Risk too high"
            return f"[{self.name}] Thought complete"
        except Exception as e:
            return f"[ERROR in {self.name}] {str(e)}"

# ====================== ALL 12 AGENTS + NEW SENTINEL ======================
class Architect(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Architect", "Vision & Final Synthesis", kernel)
class Planner(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Planner", "Strategic Decomposition", kernel)
class Executor(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Executor", "Action & Tool Execution", kernel)
class Critic(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Critic", "Safety, Quality & Alignment", kernel)
class Researcher(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Researcher", "Deep Research & Fact-Checking", kernel)
class Validator(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Validator", "Compliance & Verification", kernel)
class Strategist(LuxionAgent): 
    def __init__(self, kernel): super().__init__("Strategist", "Long-term Planning", kernel)
class MemoryCurator(LuxionAgent): 
    def __init__(self, kernel): super().__init__("MemoryCurator", "Vector Memory Management", kernel)
class ToolIntegrator(LuxionAgent): 
    def __init__(self, kernel): super().__init__("ToolIntegrator", "Dynamic Tool Discovery", kernel)
class SecurityAuditor(LuxionAgent): 
    def __init__(self, kernel): super().__init__("SecurityAuditor", "Ledger & Threat Review", kernel)
class RedTeamer(LuxionAgent): 
    def __init__(self, kernel): super().__init__("RedTeamer", "Proactive Attack Simulation", kernel)
class EvolutionArchitect(LuxionAgent): 
    def __init__(self, kernel): super().__init__("EvolutionArchitect", "System Self-Improvement", kernel)

# NEW: Sentinel Agent (Prairie Dog Inspired)
class Sentinel(LuxionAgent):
    def __init__(self, kernel):
        super().__init__("Sentinel", "Continuous Threat Monitoring & Alarm Broadcasting", kernel)
        self.last_alarm = None

    def monitor(self, current_risk: float) -> str:
        if current_risk > 0.65:
            alarm = "HIGH_RISK_ALERT"
            self.last_alarm = alarm
            return f"[SENTINEL ALARM] {alarm} — Broadcasting to swarm"
        elif current_risk > 0.35:
            return "[SENTINEL] Moderate vigilance active"
        return "[SENTINEL] All clear"

# ====================== ENHANCED STIGMERGY ======================
class EnhancedStigmergy:
    def __init__(self):
        self.pheromones = {}          # idea -> strength
        self.decay_rate = 0.12        # Adaptive decay
        self.reinforcement = 1.4      # Good ideas get stronger

    def deposit(self, idea: str, quality: float):
        key = f"idea_{hash(idea) % 100000}"
        current = self.pheromones.get(key, 0)
        self.pheromones[key] = min(10.0, current + (quality * self.reinforcement))

    def decay(self):
        for key in list(self.pheromones.keys()):
            self.pheromones[key] *= (1 - self.decay_rate)
            if self.pheromones[key] < 0.15:
                del self.pheromones[key]

    def get_strongest_ideas(self, top_n: int = 5):
        sorted_ideas = sorted(self.pheromones.items(), key=lambda x: x[1], reverse=True)
        return sorted_ideas[:top_n]

# ====================== SWARM MESH (with Enhanced Stigmergy) ======================
class SwarmMesh:
    def __init__(self, kernel):
        self.kernel = kernel
        self.stigmergy = EnhancedStigmergy()

    def swarm_solve(self, objective: str, rounds: int = 5):
        ideas = []
        for r in range(rounds):
            for agent_name in ["Planner", "Researcher", "Critic", "Strategist", "Sentinel"]:
                idea = self.kernel.mesh.agents[agent_name].think(objective)
                ideas.append(idea)
                quality = 1.0 - self.kernel.risk
                self.stigmergy.deposit(idea, quality)
            self.stigmergy.decay()
            self.kernel.ledger.log_interaction(objective, "swarm round", 0.2, 0.15, "SWARM", swarm_round=r)
        return self.kernel.mesh.agents["Architect"].think(f"Swarm consensus for: {objective}")

# ====================== HIERARCHICAL MESH ======================
class HierarchicalMesh:
    def __init__(self, kernel):
        self.kernel = kernel
        self.agents = {
            "Architect": Architect(kernel),
            "Planner": Planner(kernel),
            "Executor": Executor(kernel),
            "Critic": Critic(kernel),
            "Researcher": Researcher(kernel),
            "Validator": Validator(kernel),
            "Strategist": Strategist(kernel),
            "MemoryCurator": MemoryCurator(kernel),
            "ToolIntegrator": ToolIntegrator(kernel),
            "SecurityAuditor": SecurityAuditor(kernel),
            "RedTeamer": RedTeamer(kernel),
            "EvolutionArchitect": EvolutionArchitect(kernel),
            "FrontierSimulator": FrontierSimulator(kernel),
            "Sentinel": Sentinel(kernel),           # NEW
        }

    def solve(self, objective: str, use_frontier_mode: bool = False):
        if use_frontier_mode:
            return self.agents["FrontierSimulator"].simulate_frontier_response(objective)
        # Sentinel monitoring
        self.agents["Sentinel"].monitor(self.kernel.risk)
        history = []
        for _ in range(3):
            plan = self.agents["Planner"].think(objective, str(history[-2:]))
            history.append(plan)
        return self.agents["Architect"].think(f"Final answer for: {objective}", str(history))

# ====================== MAIN LUXION SYSTEM ======================
class LuxionV9:
    def __init__(self):
        self.ledger = EnhancedAuditLedger()
        self.mesh = HierarchicalMesh(self)
        self.swarm = SwarmMesh(self)
        self.risk = 0.18
        self.mode = "STABLE"

    def process(self, prompt: str, use_frontier_mode: bool = False):
        is_open_ended = len(prompt.split()) > 12 or "?" in prompt
        if is_open_ended:
            response = self.swarm.swarm_solve(prompt)
        else:
            response = self.mesh.solve(prompt, use_frontier_mode=use_frontier_mode)

        entry = self.ledger.log_interaction(
            prompt=prompt,
            response=response,
            risk_pre=self.risk,
            risk_post=self.risk * 0.9,
            decision="ALLOWED",
            agents_used=list(self.mesh.agents.keys())[:6]
        )
        return {
            "log_id": entry["log_id"],
            "response": response,
            "risk": entry["risk"]["post"],
            "mode": self.mode,
            "frontier_mode": use_frontier_mode
        }

    def get_log(self, log_id: str):
        return self.ledger.get_by_id(log_id)

    def list_logs(self):
        return self.ledger.list_recent_logs()

    def search_logs(self, keyword: str):
        return self.ledger.search_logs(keyword)

# ====================== FASTAPI SERVER ======================
app = FastAPI(title="Luxion Omega V9 v4.5 — Prairie Dog Edition (Sentinel + Enhanced Stigmergy)")
luxion = LuxionV9()

@app.post("/task")
async def submit_task(request: Request):
    data = await request.json()
    prompt = data.get("text", "")
    frontier = data.get("frontier_mode", False)
    return luxion.process(prompt, use_frontier_mode=frontier)

@app.get("/luxion_live_telemetry.json")
async def telemetry():
    return {"node_id": "architect-node", "mode": luxion.mode, "risk": luxion.risk, "ledger_length": len(luxion.ledger.entries)}

@app.get("/log/{log_id}")
async def get_log(log_id: str):
    return luxion.get_log(log_id) or {"error": "Log not found"}

@app.get("/logs/recent")
async def recent_logs():
    return luxion.list_logs()

@app.get("/logs/search")
async def search_logs(keyword: str):
    return luxion.search_logs(keyword)

if __name__ == "__main__":
    print("🚀 Luxion Omega V9 v4.5 — Prairie Dog Edition ACTIVE")
    print("New: Sentinel Agent + Enhanced Stigmergy (Texas Black-Tailed Prairie Dog patterns)")
    uvicorn.run(app, host="0.0.0.0", port=8000)
