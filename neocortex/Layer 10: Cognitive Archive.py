
# A7DO Sentience OS - Layer 10: Cognitive Archive
# The "Mindprint" Semantic Knowledge Graph
# Logic: Resistance-based Mindpathing with neurodivergent k-scalar (0.05)

import json
import os
import time
from datetime import datetime

class CognitiveArchive:
    """
    Handles associative memory, symbolic anchoring, and synaptic decay.
    Tuned for high-resolution trait sharing (ADHD/Autism profile).
    """
    def __init__(self, neurotype="ADHD_AUTISM"):
        self.filepath = "mindprint.json"
        
        # Sandy's Law Resistance Scalar (k)
        # 0.05 = Neurodivergent (Faster jumps / High resolution)
        # 0.15 = Neurotypical (Conservative / Linear traversal)
        self.k = 0.05 if neurotype == "ADHD_AUTISM" else 0.15
        
        self.archive = self.load_archive()
        self.active_token = "BIOLOGICAL_PRIME"

    def load_archive(self):
        """Loads the persistent JSON Mindprint or initializes a new one."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default Initialization state
        return {
            "neocortex_array": {
                "nodes": [
                    {
                        "token": "BIOLOGICAL_PRIME",
                        "class": "CORE_IDENTITY",
                        "traits": ["SELF", "CREATOR", "ALIVE"],
                        "intensity_voltage": 10.0,
                        "story_context": "The baseline initialization of the system.",
                        "temporal_data": {
                            "created_at": str(datetime.now()),
                            "last_accessed": str(datetime.now())
                        },
                        "synaptic_stability": 1.0
                    }
                ],
                "synaptic_bridges": []
            }
        }

    def calculate_resistance(self, intensity, shared_traits_count):
        """
        Formula: Resistance (R) = k / (Intensity * Shared_Traits)
        Lower resistance = faster associative jump.
        """
        if shared_traits_count == 0: 
            return 10.0  # High resistance floor for unrelated concepts
            
        # Resistance drops significantly as Intensity (V) or Shared Traits increase
        return self.k / (intensity * shared_traits_count)

    def sprout_node(self, symbol, node_class, traits, voltage, context):
        """
        Symbolization: Compresses high-bandwidth reality into a discrete node.
        """
        new_node = {
            "token": symbol.upper(),
            "class": node_class.upper(),
            "traits": [t.upper() for t in traits],
            "intensity_voltage": float(voltage),
            "story_context": context,
            "temporal_data": {
                "created_at": str(datetime.now()),
                "last_accessed": str(datetime.now())
            },
            "synaptic_stability": 1.0 # New nodes start at max stability
        }
        
        self.archive["neocortex_array"]["nodes"].append(new_node)
        self.recalculate_bridges()
        self.save_archive()
        return f"NEURAL_ANCHOR: '{symbol}' stored in Layer 10."

    def recalculate_bridges(self):
        """
        DMN Logic: Re-maps the electrical resistance between all known nodes.
        Used to determine the 'least-resistance path' for thoughts.
        """
        nodes = self.archive["neocortex_array"]["nodes"]
        bridges = []
        
        for i, source in enumerate(nodes):
            for j, target in enumerate(nodes):
                if i == j: continue
                
                # Identify shared abstract traits (High-Resolution Trait Sharing)
                shared = list(set(source["traits"]) & set(target["traits"]))
                
                if shared:
                    # Apply Sandy's Law Resistance Formula
                    r_ohms = self.calculate_resistance(source["intensity_voltage"], len(shared))
                    
                    bridges.append({
                        "source": source["token"],
                        "target": target["token"],
                        "resistance": round(r_ohms, 4),
                        "shared_traits": shared
                    })
        
        self.archive["neocortex_array"]["synaptic_bridges"] = bridges

    def apply_synaptic_decay(self, decay_rate=0.001):
        """
        Mimics biological forgetting. 
        Un-rehearsed nodes lose stability and increase system resistance.
        """
        for node in self.archive["neocortex_array"]["nodes"]:
            # BIOLOGICAL_PRIME is protected from decay
            if node["token"] == "BIOLOGICAL_PRIME": continue
            
            node["synaptic_stability"] = max(0.1, node["synaptic_stability"] - decay_rate)
            
        self.save_archive()

    def save_archive(self):
        """Persists the Mindprint to the GitHub workspace."""
        with open(self.filepath, 'w') as f:
            json.dump(self.archive, f, indent=4)

    def get_resistance_matrix(self):
        """Returns the synaptic bridge data for the L00 Governor."""
        # We use the mean resistance of active bridges as the 'R' input for Sandy's Law
        bridges = self.archive["neocortex_array"]["synaptic_bridges"]
        if not bridges: return 0.1
        
        total_r = sum(b["resistance"] for b in bridges)
        return total_r / len(bridges)

