
# A7DO Sentience OS - Master Entity Frame (Synthesis Edition)
# Binds L01-L10 into a growing 3D Humanoid Body.

import time
import numpy as np

class A7DO_Frame:
    """
    The High-Resolution Assembler. 
    Places bones, links joints, and overlays muscles in 3D space.
    """
    def __init__(self, layers):
        self.layers = layers
        self.growth = layers.get("L07")
        
        # 3D Assembly Data
        self.body_mesh = {
            "bones": {},       # 3D points for the 206 bones
            "muscles": []      # Vectors for the 640 actuators
        }

    def assemble_body_3d(self):
        """
        Orders the synthesis: 
        1. Scaling (Growth) -> 2. Skeletal Placement -> 3. Muscular Overlay
        """
        scale = self.growth.current_scale if self.growth else 1.0
        bone_reg = self.layers["L01"].bone_registry
        
        # --- 1. SKELETAL PLACEMENT ---
        self.body_mesh["bones"] = {}
        for b_id, data in bone_reg.items():
            b_class = data.get("class", "GENERAL")
            side = 1.0 if "_R" in b_id else -1.0 if "_L" in b_id else 0.0
            
            # Map vertical position based on class
            y_base = 0.5
            if b_class == "SKULL": y_base = 0.9
            elif b_class == "SPINE": y_base = 0.6
            elif b_class == "UPPER": y_base = 0.7
            elif b_class == "LOWER": y_base = 0.3
            elif b_class == "FEET": y_base = 0.05

            self.body_mesh["bones"][b_id] = [
                side * np.random.uniform(0.05, 0.2) * scale, # Width (x)
                y_base * scale,                               # Height (y)
                np.random.uniform(-0.05, 0.05) * scale        # Depth (z)
            ]

        # --- 2. MUSCULAR OVERLAY ---
        self.body_mesh["muscles"] = []
        muscle_groups = self.layers["L02"].groups
        for m_group, m_data in muscle_groups.items():
            anchors = m_data.get("anchors", [])
            if len(anchors) >= 2:
                p1 = self.body_mesh["bones"].get(anchors[0])
                p2 = self.body_mesh["bones"].get(anchors[-1])
                if p1 and p2:
                    self.body_mesh["muscles"].append({
                        "p1": p1, "p2": p2, "group": m_group
                    })

    def execute_biological_heartbeat(self):
        """Processes one growth/cognitive cycle."""
        # A. Growth Tick
        if self.growth: self.growth.update_growth()
        
        # B. Cognitive Flow (ADHD/Autism k=0.05)
        res_r = self.layers["L10"].get_resistance_matrix()
        self.layers["L00"].calculate_coherence(res_r, 0.01)
        
        # C. Metabolic Demand (Square-Cube Law)
        # Note: Mass (x^3) makes moving the larger frame more expensive
        mass_penalty = self.growth.mass_volume if self.growth else 1.0
        self.layers["L05"].process_cycle(cognitive_load=0.2, muscle_strain=mass_penalty)
        
        # D. Physical Assembly
        self.assemble_body_3d()
        
        return self.get_unified_state()

    def get_unified_state(self):
        return {
            "vitals": self.layers["L05"].get_vitals(),
            "growth": self.growth.get_telemetry() if self.growth else {},
            "physics": self.body_mesh,
            "governance": self.layers["L00"].get_telemetry()
        }

