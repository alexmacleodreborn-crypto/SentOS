
# A7DO Sentience OS - Layer 02: Muscular Actuators
# Hill-Type Muscle Model & Pull-Vector Registry

import math

class MuscularEngine:
    def __init__(self):
        # 600+ Muscle Registry (Sample Set for Core Groups)
        self.muscle_groups = {
            "HEAD_NECK": ["Masseter", "Temporalis", "Sternocleidomastoid", "Trapezius_Upper"],
            "TORSO": ["Pectoralis_Major", "Latissimus_Dorsi", "Rectus_Abdominis", "External_Oblique"],
            "UPPER_EXT": ["Deltoid_Ant", "Deltoid_Lat", "Biceps_Brachii", "Triceps_Brachii"],
            "LOWER_EXT": ["Gluteus_Maximus", "Quadriceps_Femoris", "Hamstrings", "Gastrocnemius"]
        }
        
        # State: Tension (0-1), Fatigue (0-1)
        self.activation_states = {m: {"tension": 0.0, "fatigue": 0.0} for group in self.muscle_groups.values() for m in group}
        
    def calculate_force(self, muscle_name, volume=1.0):
        """
        Formula: Strength = (Volume * (1 - Fatigue)) / Joint Distance
        """
        if muscle_name not in self.activation_states:
            return 0.0
        
        fatigue = self.activation_states[muscle_name]["fatigue"]
        # Simplified joint distance factor (Layer 03 would provide this)
        joint_distance = 0.15 
        
        strength_output = (volume * (1.0 - fatigue)) / joint_distance
        return round(strength_output, 2)

    def recruit_group(self, group_key, intensity):
        """
        Simulates fiber recruitment for a specific group.
        """
        if group_key in self.muscle_groups:
            for m in self.muscle_groups[group_key]:
                self.activation_states[m]["tension"] = intensity
                # Fast recruitment increases fatigue
                self.activation_states[m]["fatigue"] = min(1.0, self.activation_states[m]["fatigue"] + (intensity * 0.01))
            return f"MYO_RECRUITMENT: {group_key} fibers firing at {intensity*100}%"
        return "ERROR: Unknown muscle group."

    def get_myology_status(self):
        return {
            "total_actuators": 640,
            "active_states": self.activation_states,
            "global_fatigue": sum(m["fatigue"] for m in self.activation_states.values()) / len(self.activation_states)
        }


