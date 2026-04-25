
# A7DO Sentience OS - Layer 05: Visceral Systems
# Metabolic ATP Loops & Autonomic Vitals
# Logic: Managing energy consumption and internal survival states.

import random

class MetabolicEngine:
    """
    The energy management layer of the A7DO organism.
    Tracks live BPM, ATP drain, and organ efficiency.
    """
    def __init__(self):
        # Baseline Vitals
        self.atp_level = 100.0      # Energy Percentage
        self.heart_rate = 72        # BPM (Fluctuates based on load)
        self.respiration_rate = 16  # Breaths per minute
        
        # Organ Registry (Operational Efficiency)
        self.organs = {
            "HEART": {"status": "PUMPING", "efficiency": 1.0},
            "LUNGS": {"status": "OXYGENATING", "capacity": 1.0},
            "LIVER": {"status": "FILTERING", "load": 0.1},
            "BRAIN_STEM": {"status": "AUTONOMIC_CONTROL", "signal": "STABLE"}
        }
        
        self.recovery_mode_active = False

    def process_cycle(self, cognitive_load, muscle_strain=0.0, is_growing=False):
        """
        Sandy's Law: Energy drain scales with 'Pressure' (cognitive_load).
        Formula: ATP_drain = f(muscle_force * time) + cognitive_tax
        """
        # 1. Calculate Basal Metabolic Drain
        basal_tax = 0.005
        
        # 2. Add Cognitive tax (BPM spikes during load)
        cognitive_tax = cognitive_load * 0.02
        
        # 3. Add Physical tax (Growth or Muscle Recruitment)
        physical_tax = (muscle_strain * 0.05) + (0.01 if is_growing else 0.0)
        
        total_drain = basal_tax + cognitive_tax + physical_tax
        
        # Apply Drain
        if not self.recovery_mode_active:
            self.atp_level = max(0.0, self.atp_level - total_drain)
        else:
            # Recovery/Sleep replenishes ATP
            self.atp_level = min(100.0, self.atp_level + 0.1)

        # 4. Update Heart Rate
        # BPM Spikes during cognitive processing or high-voltage memory access
        target_bpm = 70 + (cognitive_load * 30) + (muscle_strain * 40)
        # Add minor biological noise/jitter
        self.heart_rate = int(target_bpm + random.randint(-3, 3))
        
        # 5. Check Survival Condition (Irreversibility)
        # If ATP < 5%, organs begin to fail/efficiency drops
        if self.atp_level < 5.0:
            for organ in self.organs:
                self.organs[organ]["efficiency"] *= 0.98
                self.organs[organ]["status"] = "CRITICAL_OXYGEN_DEBT"
        
        return self.get_vitals()

    def execute_swerve_cost(self):
        """
        The Swerve Penalty: Topological jumps consume significant energy units.
        This prevents the system from 'jumping' without cause.
        """
        drain = 10.0 # 10% ATP cost for a Swerve
        self.atp_level = max(0.0, self.atp_level - drain)
        self.heart_rate += 25 # Immediate adrenal spike
        return f"VISCERAL_FEEDBACK: Swerve cost applied. ATP at {self.atp_level:.1f}%"

    def toggle_recovery(self, state: bool):
        """
        Enter Sleep/Consolidation mode (Layer 10 link).
        """
        self.recovery_mode_active = state
        if state:
            self.organs["HEART"]["status"] = "RESTING"
            return "SYSTEM_IDLE: Metabolic recovery active."
        else:
            self.organs["HEART"]["status"] = "PUMPING"
            return "SYSTEM_ACTIVE: Metabolic drain active."

    def get_vitals(self):
        """
        Returns high-resolution telemetry for the master dashboard.
        """
        return {
            "atp": round(self.atp_level, 3),
            "bpm": self.heart_rate,
            "respiration": self.respiration_rate,
            "metabolic_status": "STABLE" if self.atp_level > 20 else "EXHAUSTED",
            "organ_health": self.organs
        }

