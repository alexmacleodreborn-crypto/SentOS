
# A7DO Sentience OS - Layer 10: Cognitive Archive
# Semantic Knowledge Graph & Hebbian Mindpathing Engine

import json
from datetime import datetime

class CognitiveArchive:
    def __init__(self):
        self.nodes = []
        self.bridges = []
        self.active_token = "BIOLOGICAL_PRIME"
        self.k_constant = 1.0 # Resistance constant

    def inject_node(self, token, node_class, traits, voltage, context):
        """
        Symbolization: Compresses reality into a discrete node.
        """
        node = {
            "token": token.upper(),
            "class": node_class.upper(),
            "traits": [t.upper() for t in traits],
            "intensity_voltage": float(voltage),
            "story_context": context,
            "temporal_data": {
                "created_at": str(datetime.now()),
                "last_accessed": str(datetime.now())
            },
            "synaptic_stability": 1.0
        }
        self.nodes.append(node)
        self.recalculate_bridges()
        return f"NEURAL_STABILIZED: Node '{token}' anchored in Neocortex."

    def recalculate_bridges(self):
        """
        Hebbian Wiring: Calculates resistance between nodes based on shared traits.
        Formula: Resistance = k / (Intensity * Shared_Traits_Count)
        """
        self.bridges = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                n1 = self.nodes[i]
                n2 = self.nodes[j]
                
                shared = set(n1["traits"]) & set(n2["traits"])
                if shared:
                    # Combined voltage effect
                    combined_v = (n1["intensity_voltage"] + n2["intensity_voltage"]) / 2
                    resistance = self.k_constant / (combined_v * len(shared))
                    
                    self.bridges.append({
                        "source": n1["token"],
                        "target": n2["token"],
                        "shared": list(shared),
                        "resistance_ohms": round(resistance, 4)
                    })

    def get_mind_map(self):
        return {
            "active_thought": self.active_token,
            "total_nodes": len(self.nodes),
            "synaptic_bridges": len(self.bridges),
            "graph": {"nodes": self.nodes, "edges": self.bridges}
        }
