
# A7DO Sentience OS - Layer 06: Optic Registry
# Active Object Identification & Symbolization Discovery

import random

class OpticRegistry:
    def __init__(self):
        self.status = "OBSERVING"
        self.known_object_tokens = ["BIOLOGICAL_PRIME", "SKELETON_CHASSIS"]
        self.detected_buffer = []
        self.discovery_needed = False
        self.active_unidentified_mesh = None

    def scan_environment(self, frame_data):
        """
        Simulates the detection of bounding boxes and meshes in the room.
        """
        # Simulated "Discovered" items in the camera view
        potential_objects = ["PHONE", "CUP", "UNKNOWN_GEOMETRY_01", "CHAIR"]
        detected = random.sample(potential_objects, 2)
        
        self.detected_buffer = []
        self.discovery_needed = False
        
        for obj in detected:
            is_known = obj in self.known_object_tokens
            self.detected_buffer.append({
                "raw_token": obj,
                "confidence": round(random.uniform(0.85, 0.99), 2),
                "is_known": is_known
            })
            if not is_known:
                self.discovery_needed = True
                self.active_unidentified_mesh = obj
                
        return self.detected_buffer

    def learn_token(self, token):
        self.known_object_tokens.append(token.upper())
        self.discovery_needed = False
        return f"OPTIC_STABILIZED: Symbol '{token}' added to Known Registry."

    def get_sensory_logs(self):
        return {
            "detecting": self.status,
            "buffer_count": len(self.detected_buffer),
            "discovery_flag": self.discovery_needed,
            "active_mesh": self.active_unidentified_mesh
        }


