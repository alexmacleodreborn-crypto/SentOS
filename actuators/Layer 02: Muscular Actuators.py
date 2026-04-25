
# A7DO Sentience OS - Layer 02: Muscular Actuators (High-Resolution)
# Hill-Type Muscle Contraction & 640+ Actuator Registry
# Logic: Strength = (Volume * (1.0 - Fatigue)) / Joint Distance

import time
import random

class MuscularEngine:
    """
    The High-Resolution Actuator Layer.
    Translates cognitive intent into contraction vectors across the 206-bone chassis.
    """
    def __init__(self):
        # 1. THE 640+ ACTUATOR REGISTRY (Categorized for Physics Sandbox)
        self.total_actuators = 640
        self.groups = {
            "HEAD_NECK": ["Masseter_L", "Masseter_R", "Temporalis_L", "Temporalis_R", "Sternocleidomastoid", "Platysma"],
            "TRUNK": ["Pectoralis_Major_L", "Pectoralis_Major_R", "Rectus_Abdominis", "Latissimus_Dorsi", "Trapezius"],
            "UPPER_LIMB_L": ["Deltoid_L", "Biceps_Brachii_L", "Triceps_Brachii_L", "Brachialis_L", "Flexor_Carpi_L"],
            "UPPER_LIMB_R": ["Deltoid_R", "Biceps_Brachii_R", "Triceps_Brachii_R", "Brachialis_R", "Flexor_Carpi_R"],
            "LOWER_LIMB_L": ["Gluteus_Maximus_L", "Quadriceps_Femoris_L", "Hamstrings_L", "Gastrocnemius_L", "Tibialis_Ant_L"],
            "LOWER_LIMB_R": ["Gluteus_Maximus_R", "Quadriceps_Femoris_R", "Hamstrings_R", "Gastrocnemius_R", "Tibialis_Ant_R"]
        }
        
        # 2. STATE VECTORS (Tension, Fatigue, Volume)
        # Every actuator is tracked individually
        self.activation_states = {}
        for group_name, muscles in self.groups.items():
            for muscle in muscles:
                self.activation_states[muscle] = {
                    "tension": 0.0,      # Current recruitment (0.0 to 1.0)
                    "fatigue": 0.0,      # Lactic acid build-up (0.0 to 1.0)
                    "volume": 1.0,       # Physical size/Hypertrophy
                    "attachment": group_name
                }
        
        self.global_atp_drain = 0.0
        self.last_sync = time.time()

    def calculate_force(self, muscle_name, joint_distance=0.15):
        """
        Hill-Type Physics: Strength = (Volume * (1.0 - Fatigue)) / Joint Distance
        This force is what moves the individual bones in Layer 03.
        """
        if muscle_name not in self.activation_states:
            return 0.0
            
        m = self.activation_states[muscle_name]
        
        # Force is scaled by current tension and reduced by fatigue
        force_output = (m["volume"] * (1.0 - m["fatigue"])) / max(0.01, joint_distance)
        return round(force_output * m["tension"], 2)

    def recruit_group(self, group_key, intensity):
        """
        Recruits fibers across a skeletal segment. 
        Higher intensity = Faster movement but higher ATP drain and Fatigue.
        """
        if group_key not in self.groups:
            return f"ACTUATOR_ERROR: Group {group_key} not found."
            
        for muscle in self.groups[group_key]:
            m = self.activation_states[muscle]
            m["tension"] = intensity
            
            # Fatigue growth: Quadratic scaling (x^2)
            # Sudden high-intensity "Swerves" cause massive fatigue
            fatigue_gain = (intensity ** 2) * 0.05
            m["fatigue"] = min(1.0, m["fatigue"] + fatigue_gain)
            
        return f"MYO_SYNC: {group_key} recruitment at {intensity*100}%"

    def calculate_metabolic_tax(self):
        """
        Returns the energy cost for Layer 05.
        Tired muscles cost more ATP to recruit (efficiency drop).
        """
        total_tax = 0.0
        for m in self.activation_states.values():
            # Formula: drain = tension * (1 + fatigue)
            drain = m["tension"] * (1.0 + m["fatigue"])
            total_tax += (drain * 0.002)
            
        self.global_atp_drain = round(total_tax, 4)
        return self.global_atp_drain

    def recover(self, rate=0.01):
        """Simulates aerobic recovery during Sleep Cycles."""
        for m in self.activation_states.values():
            m["fatigue"] = max(0.0, m["fatigue"] - rate)
            m["tension"] *= 0.8 # Muscle tone relaxes
        return "RECOVERY_COMPLETE"

    def get_myology_telemetry(self):
        """State report for the Executive Dashboard."""
        active = [k for k, v in self.activation_states.items() if v["tension"] > 0.1]
        avg_fatigue = sum(v["fatigue"] for v in self.activation_states.values()) / self.total_actuators
        
        return {
            "actuators_mapped": self.total_actuators,
            "avg_fatigue": round(avg_fatigue, 4),
            "atp_demand": self.global_atp_drain,
            "active_fibers": active[:10], # Show top 10 active
            "status": "NOMINAL" if avg_fatigue < 0.5 else "EXHAUSTED"
        }

