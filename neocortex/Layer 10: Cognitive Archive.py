
# A7DO Sentience OS - Layer 10: Cognitive Archive
# Dynamic Memory Sprouting & Linguistic Anchoring

from datetime import datetime

class CognitiveArchive:
    def __init__(self):
        self.nodes = []
        self.bridges = []
        self.active_context = "OBSERVATION_MODE"

    def inject_node(self, token, node_class, traits, voltage, context):
        node = {
            "token": token.upper(),
            "class": node_class.upper(),
            "traits": [t.upper() for t in traits],
            "intensity_voltage": float(voltage),
            "story_context": context,
            "temporal_data": {"created_at": str(datetime.now())},
            "synaptic_stability": 1.0
        }
        self.nodes.append(node)
        self.recalculate_bridges()
        return f"NEURAL_STABILIZED: {token} anchored."

    def recalculate_bridges(self):
        self.bridges = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                n1, n2 = self.nodes[i], self.nodes[j]
                shared = set(n1["traits"]) & set(n2["traits"])
                if shared:
                    combined_v = (n1["intensity_voltage"] + n2["intensity_voltage"]) / 2
                    resistance = 1.0 / (combined_v * len(shared))
                    self.bridges.append({"source": n1["token"], "target": n2["token"], "resistance": round(resistance, 4)})

    def get_mind_map(self):
        return {"total_nodes": len(self.nodes), "bridges": len(self.bridges)}
