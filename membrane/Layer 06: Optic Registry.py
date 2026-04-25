
# A7DO Sentience OS - Layer 06: Optic Registry
# Active Perceptual Ingress & Spatial Fixation
# Logic: Tracks 3D geometries and exports HUD coordinates for the user.

import random
import time

class OpticRegistry:
    """
    Handles the visual manifold. 
    Includes Fixation logic so the user can see what A7DO sees in the room.
    """
    def __init__(self):
        self.active_ingress = []
        self.discovery_needed = False
        self.target_mesh = None
        
        # HUD Coordinates for the Dashboard Reticle (x, y, width, height)
        self.fixation_data = {"x": 0, "y": 0, "w": 0, "h": 0} 
        
        # Sandy's Law Parameters
        self.trap_strength_z = 0.05 # Noise floor (Z)

    def scan_environment(self, neocortex_nodes):
        """
        Simulates the detection of geometries.
        If an object is unknown, A7DO 'Fixates' on it by locking coordinates.
        """
        # Simulated objects in the room with positions for the HUD
        # In a live system, these come from YOLO or MediaPipe
        room_objects = [
            {"id": "MESH_USER", "x": 30, "y": 20, "w": 40, "h": 60},
            {"id": "MESH_CHASSIS", "x": 10, "y": 70, "w": 20, "h": 20},
            {"id": f"MESH_UNK_{random.randint(10, 99)}", "x": random.randint(50, 70), "y": random.randint(10, 40), "w": 15, "h": 15}
        ]
        
        self.active_ingress = []
        unknown_found = False
        
        for obj in room_objects:
            # Cross-reference with Layer 10 Symbols (Mindprint)
            is_known = any(node["token"] in obj["id"] for node in neocortex_nodes)
            
            if not is_known and not unknown_found:
                # A7DO "Fixates" on the FIRST unknown object he sees
                unknown_found = True
                self.discovery_needed = True
                self.target_mesh = obj["id"]
                self.fixation_data = {
                    "x": obj["x"], "y": obj["y"], 
                    "w": obj["w"], "h": obj["h"]
                }
            
            self.active_ingress.append({
                "id": obj["id"],
                "known": is_known,
                "coords": {"x": obj["x"], "y": obj["y"], "w": obj["w"], "h": obj["h"]}
            })
            
        # Sandy's Law: Noise (Z) spikes if he can't identify his focus
        # This pressure drives the "Language Bridge" to activate
        self.trap_strength_z = 0.75 if unknown_found else 0.05
        
        if not unknown_found:
            self.discovery_needed = False
            self.target_mesh = None
            self.fixation_data = {"x": 0, "y": 0, "w": 0, "h": 0}
            
        return self.active_ingress

    def get_sensory_telemetry(self):
        """
        Returns the data needed to draw the reticle and calculate Sandy's Law.
        """
        return {
            "trap_strength_z": round(self.trap_strength_z, 3),
            "discovery_active": self.discovery_needed,
            "target_mesh": self.target_mesh,
            "fixation_box": self.fixation_data, # For the HUD overlay
            "manifold_status": "STABLE" if self.trap_strength_z < 0.5 else "HIGH_ENTROPY"
        }

