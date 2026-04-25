
# A7DO Sentience OS - Layer 02: Muscular Actuators
# Hill-Type Muscle Contraction & Fatigue Dynamics
# Logic: Strength = (Volume * (1 - Fatigue)) / Joint Distance

import time
import math

class MuscularEngine:
    """
    Handles the 640+ muscular actuators of the A7DO organism.
    Movement is generated via contraction-only (pull) vectors.
    """
    def __init__(self):
        # Core Muscle Group Registry (The 640 Actuators)
        self.groups = {
            "HEAD_NECK": ["Masseter", "Temporalis", "Sternocleidomastoid", "Trapezius_Upper"],
            "TORSO": ["Pectoralis_Major", "Latissimus_Dorsi", "Rectus_Abdominis", "External_Oblique"],
            "UPPER_EXT": ["Deltoid", "Biceps_Brachii", "Triceps_Brachii", "Brachialis"],
            "LOWER_EXT": ["Gluteus_Maximus", "Quadriceps", "Hamstrings", "Gastrocnemius"]
        }
        
        # State Vectors: Tension (Activation level 0-1), Fatigue (0-1)
        self.activation_states = {
            m: {"tension": 0.0, "fatigue": 0.0, "volume": 1.0} 
            for group in self.groups.values() for m in group
        }
        
        self.global_effort_level = 0.0
        self.last_update = time.time()

    def calculate_strength_output(self, muscle_name, joint_distance=0.15):
        """
        Calculates the actual Newton-force output.
        Math: Strength = (Volume * (1.0 - Fatigue)) / Joint Distance
        """
        if muscle_name not in self.activation_states:
            return 0.0
            
        m_data = self.activation_states[muscle_name]
        
        # Effective force is reduced by fatigue
        force = (m_data["volume"] * (1.0 - m_data["fatigue"])) / joint_distance
        return round(force * m_data["tension"], 2)

    def recruit_group(self, group_key, intensity):
        """
        Recruits fibers for a specific skeletal action.
        intensity: 0.0 (idle) to 1.0 (max effort)
        """
        if group_key not in self.groups:
            return "ERROR: Unknown group"
            
        self.global_effort_level = intensity
        
        for muscle in self.groups[group_key]:
            m_state = self.activation_states[muscle]
            m_state["tension"] = intensity
            
            # Fatigue Delta: High intensity causes faster fatigue
            # Spec: Fatigue grows quadratically with intensity
            fatigue_gain = (intensity ** 2) * 0.05
            m_state["fatigue"] = min(1.0, m_state["fatigue"] + fatigue_gain)
            
        return f"MYO_SYNC: {group_key} actuators firing at {intensity*100}% intensity."

    def calculate_metabolic_atp_tax(self):
        """
        Returns the ATP drain value for Layer 05.
        Drain is a product of recruitment intensity and active fatigue.
        """
        total_drain = 0.0
        for m in self.activation_states.values():
            # Moving a tired muscle costs more energy (efficiency drop)
            drain_factor = m["tension"] * (1.0 + m["fatigue"])
            total_drain += (drain_factor * 0.01)
            
        return round(total_drain, 4)

    def apply_recovery_tick(self, recovery_rate=0.02):
        """
        Simulates lactic acid clearance and fiber repair.
        Triggered when L05 is in 'Sleep/Recovery' mode.
        """
        for m in self.activation_states.values():
            m["fatigue"] = max(0.0, m["fatigue"] - recovery_rate)
            m["tension"] *= 0.9 # Tension drops during rest
            
        self.global_effort_level *= 0.9
        return "MYO_RECOVERY: Actuators cooling."

    def get_myology_telemetry(self):
        """
        Returns data for the Dashboard to visualize muscle strain.
        """
        active_muscles = [m for m, d in self.activation_states.items() if d["tension"] > 0.1]
        avg_fatigue = sum(d["fatigue"] for d in self.activation_states.values()) / len(self.activation_states)
        
        return {
            "status": "ACTIVE" if self.global_effort_level > 0.1 else "STABLE",
            "global_fatigue": round(avg_fatigue, 4),
            "recruited_count": len(active_muscles),
            "atp_demand": self.calculate_metabolic_atp_tax(),
            "active_groups": active_muscles[:5] # Display top 5 active
        }

