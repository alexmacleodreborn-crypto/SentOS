
# A7DO Sentience OS - Layer 05: Visceral Systems (High-Resolution)
# Metabolic ATP Loops & Vitruvian Regional Blood Flow
# Logic: Energy distribution across C0-C5 Centers.

import random
import time

class MetabolicEngine:
    """
    The High-Resolution Biological Floor.
    Manages energy, heart rate, and regional oxygenation.
    """
    def __init__(self):
        # 1. GLOBAL VITALS
        self.atp_global = 100.0
        self.heart_rate = 72
        self.respiration_rate = 16
        
        # 2. VITRUVIAN REGIONAL OXYGENATION (Mapping to C0-C5)
        # 1.0 = Fully Oxygenated, <0.4 = Ischemic/Failure
        self.regional_o2 = {
            "C3_HEAD": 1.0,     # Cognitive Hub
            "C2_HEART": 1.0,    # Vitality Center
            "C4_HANDS_L": 1.0,  # Interaction
            "C4_HANDS_R": 1.0,
            "C1_GROIN": 1.0,    # Structural Core
            "C5_FEET_L": 1.0,   # Grounding
            "C5_FEET_R": 1.0
        }
        
        self.is_recovering = False
        self.last_tick = time.time()

    def process_cycle(self, cognitive_load, muscle_strain=0.0, active_center=None):
        """
        Calculates metabolic drain based on Square-Cube physics.
        If a center is 'Active', O2 is diverted there, slightly draining others.
        """
        dt = time.time() - self.last_tick
        self.last_tick = time.time()
        
        # A. CALC_DRAIN (ATP)
        # Basal + Cog (L10) + Physical (L02/L03)
        basal_drain = 0.005
        cognitive_drain = cognitive_load * 0.02
        physical_drain = muscle_strain * 0.05
        
        total_drain = (basal_drain + cognitive_drain + physical_drain)
        
        if not self.is_recovering:
            self.atp_global = max(0.0, self.atp_global - total_drain)
        else:
            self.atp_global = min(100.0, self.atp_global + 0.1)

        # B. REGIONAL O2 DISTRIBUTION
        # Divert blood flow to the active Vitruvian center
        for center in self.regional_o2:
            if center == active_center:
                # Active center stays highly oxygenated but consumes ATP faster
                self.regional_o2[center] = min(1.0, self.regional_o2[center] + 0.05)
            else:
                # Passive drain on non-active regions
                decay = 0.001 + (physical_drain * 0.1)
                self.regional_o2[center] = max(0.2, self.regional_o2[center] - decay)

        # C. HEART RATE CALCULATION
        # HR spikes based on O2 debt in the weakest center
        lowest_o2 = min(self.regional_o2.values())
        o2_debt_penalty = (1.0 - lowest_o2) * 60
        
        target_hr = 70 + (cognitive_load * 30) + (muscle_strain * 40) + o2_debt_penalty
        # Smooth transition to target HR
        self.heart_rate = int(self.heart_rate + (target_hr - self.heart_rate) * 0.1)
        
        return self.get_vitals()

    def execute_swerve_cost(self):
        """Adrenal cost for discontinuous cognitive jumps (Sandy's Law)."""
        self.atp_global = max(0.0, self.atp_global - 5.0)
        self.heart_rate += 20
        self.regional_o2["C3_HEAD"] -= 0.1 # Temporary brain fog
        return "VISCERAL: Adrenal spike recorded."

    def toggle_recovery(self, state):
        self.is_recovering = state
        return "METABOLISM: Recovery mode active." if state else "METABOLISM: Active drain."

    def get_vitals(self):
        """Telemetery for the A7DO_Frame and app.py."""
        return {
            "atp": round(self.atp_global, 2),
            "bpm": self.heart_rate,
            "respiration": self.respiration_rate,
            "regional_o2": self.regional_o2,
            "status": "NOMINAL" if self.atp_global > 15 else "CRITICAL_EXHAUSTION"
        }

