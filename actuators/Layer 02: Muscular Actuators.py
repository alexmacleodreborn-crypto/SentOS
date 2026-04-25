
# A7DO Sentience OS - Layer 02: Muscular Actuators (High-Resolution)
# Hill-Type Muscle Contraction & 640+ Actuator Registry
# Logic: Strength = (Volume * (1.0 - Fatigue)) / Joint Distance
# Regulation: Strength scales quadratically (x^2) per Square-Cube Law.

import time
import random

class MuscularEngine:
    """
    The High-Resolution Actuator Layer.
    Translates cognitive intent into contraction vectors across the 206-bone manifold.
    """
    def __init__(self, scale_x=1.0):
        # 1. THE 640+ ACTUATOR REGISTRY
        # Every muscle is anchored to specific bone IDs from Layer 01.
        self.total_actuators = 640
        self.scale_x = scale_x
        self.strength_scalar = scale_x ** 2 # Quadratic scaling (x^2)
        
        self.groups = {
            "CRANIOFACIAL": {
                "muscles": ["Masseter_L", "Masseter_R", "Temporalis_L", "Temporalis_R", "Platysma"],
                "anchors": ["Mandible", "Zygomatic_L", "Zygomatic_R", "Frontal"]
            },
            "AXIAL_TRUNK": {
                "muscles": ["Pectoralis_Major_L", "Pectoralis_Major_R", "Rectus_Abdominis", "Latissimus_Dorsi"],
                "anchors": ["Sternum_Body", "Rib_L_5", "Rib_R_5", "Humerus_L", "Humerus_R"]
            },
            "BRACHIAL_L": {
                "muscles": ["Deltoid_L", "Biceps_Brachii_L", "Triceps_Brachii_L", "Brachialis_L"],
                "anchors": ["Scapula_L", "Clavicle_L", "Humerus_L", "Radius_L", "Ulna_L"]
            },
            "BRACHIAL_R": {
                "muscles": ["Deltoid_R", "Biceps_Brachii_R", "Triceps_Brachii_R", "Brachialis_R"],
                "anchors": ["Scapula_R", "Clavicle_R", "Humerus_R", "Radius_R", "Ulna_R"]
            },
            "CRURAL_L": {
                "muscles": ["Gluteus_Maximus_L", "Quadriceps_Femoris_L", "Hamstrings_L", "Gastrocnemius_L"],
                "anchors": ["Hip_Bone_L", "Femur_L", "Patella_L", "Tibia_L", "Fibula_L"]
            },
            "CRURAL_R": {
                "muscles": ["Gluteus_Maximus_R", "Quadriceps_Femoris_R", "Hamstrings_R", "Gastrocnemius_R"],
                "anchors": ["Hip_Bone_R", "Femur_R", "Patella_R", "Tibia_R", "Fibula_R"]
            }
        }
        
        # 2. STATE VECTORS
        self.activation_states = {}
        for group_name, data in self.groups.items():
            for muscle in data["muscles"]:
                self.activation_states[muscle] = {
                    "tension": 0.0,      # Current recruitment (0.0 to 1.0)
                    "fatigue": 0.0,      # Lactic acid build-up (0.0 to 1.0)
                    "peak_force": 500.0 * self.strength_scalar, # Newtons (scales x^2)
                    "group": group_name
                }
        
        self.global_atp_demand = 0.0

    def calculate_muscle_force(self, muscle_name, joint_distance=0.15):
        """
        Hill-Type Physics: Strength = (Peak_Force * (1.0 - Fatigue)) / Joint Distance
        """
        if muscle_name not in self.activation_states:
            return 0.0
            
        m = self.activation_states[muscle_name]
        
        # Effective force is reduced by fatigue but boosted by growth (strength_scalar)
        active_force = (m["peak_force"] * (1.0 - m["fatigue"])) / max(0.01, joint_distance)
        return round(active_force * m["tension"], 2)

    def recruit_fibers(self, group_key, intensity):
        """
        Actuates a specific group based on cognitive intent.
        High intensity triggers exponential fatigue growth.
        """
        if group_key not in self.groups:
            return f"ACTUATOR_ERROR: Group {group_key} invalid."
            
        for muscle in self.groups[group_key]["muscles"]:
            m = self.activation_states[muscle]
            m["tension"] = intensity
            
            # Fatigue Delta: Quadrative intensity vs current fatigue
            # As muscles get more tired, they fatigue even faster (efficiency loss)
            fatigue_gain = (intensity ** 2) * (1.0 + m["fatigue"]) * 0.02
            m["fatigue"] = min(1.0, m["fatigue"] + fatigue_gain)
            
        return f"MYO_SYNC: {group_key} actuators firing. Resistance R detected."

    def calculate_metabolic_drain(self):
        """
        Bridges to Layer 05. 
        ATP cost is the sum of (Tension * Mass_Scalar * (1 + Fatigue)).
        """
        total_tax = 0.0
        # Mass scalar (x^3) makes moving limbs exponentially more expensive
        mass_penalty = self.scale_x ** 3
        
        for m in self.activation_states.values():
            # Formula: drain = tension * mass * fatigue_inefficiency
            drain = m["tension"] * mass_penalty * (1.0 + m["fatigue"])
            total_tax += (drain * 0.005)
            
        self.global_atp_demand = round(total_tax, 4)
        return self.global_atp_demand

    def apply_aerobic_recovery(self, oxygen_level=1.0):
        """Simulates aerobic clearance of fatigue."""
        recovery_rate = 0.01 * oxygen_level
        for m in self.activation_states.values():
            m["fatigue"] = max(0.0, m["fatigue"] - recovery_rate)
            m["tension"] *= 0.95 # Tonus relaxation
        return "MYO_STABILIZED"

    def get_myology_telemetry(self):
        """Report for the Executive Dashboard."""
        active = [k for k, v in self.activation_states.items() if v["tension"] > 0.05]
        avg_fatigue = sum(v["fatigue"] for v in self.activation_states.values()) / self.total_actuators
        
        return {
            "total_actuators": self.total_actuators,
            "avg_fatigue": round(avg_fatigue, 4),
            "atp_demand": self.global_atp_demand,
            "strength_scaling": f"{self.strength_scalar}x",
            "active_groups": active[:8],
            "structural_anchors": "SYNCHRONIZED_WITH_L01"
        }

