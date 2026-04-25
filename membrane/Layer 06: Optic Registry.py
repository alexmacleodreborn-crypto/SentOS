
# A7DO Sentience OS - Layer 06: Optic Registry
# Active Object Identification & Symbolization Discovery

import random

class OpticRegistry:
    def __init__(self):
        self.status = "OBSERVING"
        # Initial known world tokens
        self.known_tokens = ["BIOLOGICAL_PRIME", "SKELETON_CHASSIS", "THE_BUBBLE"]
        self.detected_buffer = []
        self.discovery_needed = False
        self.unidentified_geometry = None

    def scan_environment(self):
        """
        Simulates the detection of bounding boxes and meshes in the camera view.
        """
        room_objects = ["PHONE", "MUG", "MYSTERY_OBJECT_A", "CHAIR", "BOOK", "UNKNOWN_SHAPE_04"]
        # Select two random objects currently in 'view'
        current_view = random.sample(room_objects, 2)
        
        self.detected_buffer = []
        self.discovery_needed = False
        
        for obj in current_view:
            is_known = obj in self.known_tokens
            self.detected_buffer.append({
                "raw": obj,
                "confidence": round(random.uniform(0.85, 0.99), 2),
                "is_known": is_known
            })
            if not is_known:
                self.discovery_needed = True
                self.unidentified_geometry = obj
                
        return self.detected_buffer

    def symbolize_object(self, original_raw, user_identity):
        """
        Updates the registry once the user provides a linguistic label.
        """
        self.known_tokens.append(user_identity.upper())
        self.discovery_needed = False
        return f"OPTIC_STABILIZED: Shape {original_raw} mapped to {user_identity}."
