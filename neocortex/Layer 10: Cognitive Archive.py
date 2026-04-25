
# A7DO Sentience OS - Layer 10: Cognitive Archive
# Associative Memory with Neurodivergent Resistance Mapping

import json
import os
from datetime import datetime

class CognitiveArchive:
    def __init__(self, neurotype="ADHD_AUTISM"):
        self.filepath = "mindprint.json"
        # Shared trait resistance scalar (Lower = faster Mindpathing)
        self.k = 0.05 if neurotype == "ADHD_AUTISM" else 0.15
        self.nodes = self.load_archive()

    def load_archive(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {"nodes": [], "synaptic_bridges": []}

    def calculate_resistance(self, intensity, shared_traits_count):
        """ Resistance = k / (Intensity * Shared_Traits) """
        if shared_traits_count == 0: return 10.0
        return self.k / (intensity * shared_traits_count)

    def sprout_node(self, token, node_class, traits, voltage, context):
        new_node = {
            "token": token.upper(),
            "class": node_class.upper(),
            "traits": traits,
            "intensity_voltage": voltage,
            "story_context": context,
            "created_at": str(datetime.now()),
            "stability": 1.0
        }
        self.nodes["nodes"].append(new_node)
        self.save_archive()
        return f"COGNITIVE_ANCHOR: {token} Sprouts."

    def save_archive(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.nodes, f, indent=4)


