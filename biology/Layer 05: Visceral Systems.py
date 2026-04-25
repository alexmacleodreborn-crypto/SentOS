
# A7DO Sentience OS - Layer 05: Visceral Systems
# Metabolic ATP loops and Organ Vitals

import random

class MetabolicEngine:
    def __init__(self):
        self.atp_level = 100.0  # Percentage
        self.heart_rate = 72    # BPM
        self.respiration = 16   # Breaths per minute
        
        self.organs = {
            "HEART": {"status": "PUMPING", "efficiency": 1.0},
            "LUNGS": {"status": "OXYGENATING", "capacity": 1.0},
            "LIVER": {"status": "FILTERING", "load": 0.1},
            "BRAIN_STEM": {"status": "AUTONOMIC_CONTROL", "signal": "STABLE"}
        }

    def process_cycle(self, cognitive_load):
        # Sandy's Law: Energy drain scales with 'Pressure' (cognitive_load)
        drain = 0.005 + (cognitive_load * 0.01)
        self.atp_level = max(0.0, self.atp_level - drain)
        
        # Fluctuations
        self.heart_rate = int(70 + (cognitive_load * 20) + random.randint(-2, 2))
        
    def get_vitals(self):
        return {
            "atp": round(self.atp_level, 3),
            "bpm": self.heart_rate,
            "breaths": self.respiration
        }
