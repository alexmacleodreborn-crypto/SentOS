
# A7DO Sentience OS - Master Entity Frame (Vitruvian 2.0 Edition)
# Binds L01-L10 into a 3D Humanoid Shape
# Logic: Proportional mapping based on C0-C5 Centers

import time
import numpy as np

class A7DO_Frame:
    """
    Coordinates the 206-bone skeleton and 640-muscle system.
    Ensures 3D output follows a humanoid silhouette.
    """
    def __init__(self, layers, scale_x=1.0):
        self.layers = layers
        self.scale_x = scale_x
        
        # VITRUVIAN 2.0 CENTERS (Relative heights based on H=1.0)
        self.centers = {
            "C3_HEAD": 0.90,     # Cognition Hub
            "C2_HEART": 0.75,    # Vitality Center
            "C0_NAVEL": 0.60,    # Geometry Center
            "C1_GROIN": 0.50,    # Structural Center
            "C4_HANDS": 0.65,    # Interaction Hub
            "C5_FEET": 0.05      # Grounding
        }
        
        self.render_buffer = {
            "skeletal_nodes": {},
            "actuator_vectors": {},
            "centers": self.centers
        }

    def sync_3d_manifold(self):
        """
        Translates Bone IDs into a Humanoid 3D Silhouette.
        Maps every bone class to a specific spatial zone.
        """
        if "L01" not in self.layers: return
        
        bones = self.layers["L01"].bone_registry
        self.render_buffer["skeletal_nodes"] = {}
        
        for bone_id, data in bones.items():
            b_class = data.get("class", "GENERAL")
            
            # --- POSITIONAL LOGIC (Humanoid Mapping) ---
            # X: Width (-0.5 to 0.5)
            # Y: Height (0.0 to 1.0)
            # Z: Depth (-0.1 to 0.1)
            
            x, y, z = 0.0, 0.5, 0.0
            
            if b_class == "SKULL":
                x = np.random.uniform(-0.05, 0.05)
                y = self.centers["C3_HEAD"] + np.random.uniform(-0.05, 0.05)
                z = np.random.uniform(-0.02, 0.05)
                
            elif b_class == "SPINE":
                x = 0.0
                # Distribute vertebrae down the central axis
                y = np.random.uniform(self.centers["C1_GROIN"], self.centers["C3_HEAD"])
                z = -0.02
                
            elif b_class == "THORAX":
                # Rib cage spread around the heart
                side = 1.0 if "_R" in bone_id else -1.0
                x = side * np.random.uniform(0.05, 0.15)
                y = self.centers["C2_HEART"] + np.random.uniform(-0.1, 0.1)
                z = np.random.uniform(-0.05, 0.05)
                
            elif b_class == "UPPER":
                # Arms spreading out to C4
                side = 1.0 if "_R" in bone_id else -1.0
                x = side * np.random.uniform(0.1, 0.4)
                y = np.random.uniform(self.centers["C4_HANDS"] - 0.1, self.centers["C3_HEAD"] - 0.1)
                z = np.random.uniform(-0.05, 0.05)
                
            elif b_class == "LOWER":
                # Legs spreading down to C5
                side = 1.0 if "_R" in bone_id else -1.0
                x = side * np.random.uniform(0.05, 0.15)
                y = np.random.uniform(self.centers["C5_FEET"], self.centers["C1_GROIN"])
                z = np.random.uniform(-0.02, 0.02)
                
            elif b_class == "SENSORY":
                # Tiny nodes inside the head
                x = np.random.uniform(-0.02, 0.02)
                y = self.centers["C3_HEAD"]
                z = 0.0

            # Apply final scaling and store in buffer
            self.render_buffer["skeletal_nodes"][bone_id] = [
                x * self.scale_x, 
                y * self.scale_x, 
                z * self.scale_x
            ]

    def execute_biological_heartbeat(self):
        """Processes one frame of the A7DO life-cycle."""
        # 1. Perception
        if "L06" in self.layers and "L10" in self.layers:
            nodes = self.layers["L10"].archive["neocortex_array"]["nodes"]
            self.layers["L06"].scan_environment(nodes)
        
        # 2. Physics & Cognition (k=0.05 ADHD/Autism profile)
        if "L00" in self.layers and "L10" in self.layers:
            r = self.layers["L10"].get_resistance_matrix()
            self.layers["L00"].calculate_coherence(r, 0.01)
        
        # 3. Visceral
        if "L05" in self.layers:
            self.layers["L05"].process_cycle(cognitive_load=0.1)
            
        # 4. Synchronize the 3D Layout
        self.sync_3d_manifold()
        
        return self.get_unified_state()

    def reach_and_symbolize(self, label, traits):
        if "L10" in self.layers:
            self.layers["L10"].sprout_node(label, "ENVIRONMENT", traits, 5.0, "Vitruvian Interaction")
        return f"FRAME: Symbol {label} anchored at C4."

    def get_unified_state(self):
        return {
            "vitals": self.layers["L05"].get_vitals() if "L05" in self.layers else {},
            "physics": self.render_buffer,
            "governance": self.layers["L00"].get_telemetry() if "L00" in self.layers else {},
            "optics": self.layers["L06"].get_sensory_telemetry() if "L06" in self.layers else {},
            "kinematics": self.layers["L03"].get_kinematic_telemetry() if "L03" in self.layers else {}
        }
