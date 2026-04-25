
# A7DO Sentience OS - Layer 06: Optic Registry
# Perceptual Ingress & Geometric Symbolization
# Logic: Provides Trap Strength (Z) to the Layer 00 Governor.

import random
import time

class OpticRegistry:
    """
    Handles the sensory manifold. 
    Translates unidentified 3D geometries into high-entropy noise (Z).
    """
    def __init__(self):
        self.active_ingress = []
        self.discovery_needed = False
        self.target_mesh = None
        
        # Internal state for Sandy's Law feedback
        self.trap_strength_z = 0.05 
        self.last_scan_time = time.time()
        
        # Spatial orientation metrics (Depth/Disparity)
        self.disparity_scalar = 1.0

    def scan_environment(self, neocortex_nodes):
        """
        Simulates the detection of geometric meshes in the 16x16 manifold.
        Checks detected Mesh IDs against Symbol tokens in Layer 10.
        """
        # Simulated ingress stream: Known anchors + Random Unidentified Mesh
        # MESH_USER and MESH_CHASSIS are hardcoded as known for survival.
        detected_meshes = ["MESH_USER", "MESH_CHASSIS", f"MESH_UNK_{random.randint(10, 99)}"]
        
        self.active_ingress = []
        unknown_count = 0
        
        for mesh_id in detected_meshes:
            # Check if this mesh ID is symbolized in the Mindprint (L10)
            is_known = any(node["token"] in mesh_id for node in neocortex_nodes)
            
            if not is_known:
                unknown_count += 1
                self.discovery_needed = True
                self.target_mesh = mesh_id
                
            self.active_ingress.append({
                "id": mesh_id,
                "status": "RECOGNIZED" if is_known else "UNIDENTIFIED",
                "known": is_known,
                "timestamp": time.time()
            })
            
        # Calculate Trap Strength Z (Noise Floor)
        # Z approaches 1.0 if the room is full of unidentified objects (chaos)
        # Z approaches 0.0 if the environment is fully symbolized (order)
        self.trap_strength_z = min(0.95, 0.05 + (unknown_count * 0.25))
        
        if unknown_count == 0:
            self.discovery_needed = False
            self.target_mesh = None
            
        return self.active_ingress

    def get_sensory_telemetry(self):
        """
        Returns the noise/entropy metadata for the L00 Mathematical Governor.
        """
        return {
            "trap_strength_z": round(self.trap_strength_z, 3),
            "discovery_active": self.discovery_needed,
            "target_mesh": self.target_mesh,
            "manifold_status": "STABLE" if self.trap_strength_z < 0.5 else "HIGH_ENTROPY"
        }

    def process_acoustic_buffer(self, duration_ms):
        """
        Implementation of the 2000ms Silence Threshold rule.
        Flushes buffer to L10 for linguistic extraction once silence is detected.
        """
        if duration_ms > 2000:
            return "BUFFER_FLUSH_TRIGGERED"
        return "LISTENING"

