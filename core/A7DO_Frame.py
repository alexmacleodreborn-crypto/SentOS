
# A7DO Sentience OS - Master Entity Frame (3D Synthesis Edition)
# Logic: Assembling 206 Bones and 640 Muscles into a Humanoid Silhouette.

import time
import numpy as np

class A7DO_Frame:
    """
    The Master Assembler. 
    Places bones in a skeleton style, then overlays joints and muscles.
    """
    def __init__(self, layers):
        self.layers = layers
        self.growth = layers.get("L07") # Linking to the new Growth Engine
        
        # 3D Render Buffer
        self.render_data = {
            "bones": {},       # ID: {"pos": [x,y,z], "len": float}
            "joints": [],      # Connections between bones
            "muscles": []      # Pull-vectors between bone anchors
        }

    def synthesize_3d_body(self):
        """
        Builds the body from the ground up based on the current growth scale.
        Order: Skeleton -> Joints -> Muscles
        """
        scale = self.growth.current_scale if self.growth else 1.0
        bone_registry = self.layers["L01"].bone_registry
        
        # 1. SKELETAL PLACEMENT (Vitruvian silhouette)
        self.render_data["bones"] = {}
        for bone_id, data in bone_registry.items():
            b_class = data.get("class", "GENERAL")
            side = 1.0 if "_R" in bone_id else -1.0 if "_L" in bone_id else 0.0
            
            # Standard Vitruvian Y-Placement
            y_pos = 0.5
            if b_class == "SKULL": y_base = 0.9
            elif b_class == "SPINE": y_base = 0.5 + np.random.uniform(0, 0.3)
            elif b_class == "UPPER": y_base = 0.7
            elif b_class == "LOWER": y_base = 0.3
            else: y_base = 0.5
            
            # Calculate 3D coordinates scaled by growth
            self.render_data["bones"][bone_id] = {
                "x": side * np.random.uniform(0.1, 0.3) * scale,
                "y": y_base * scale,
                "z": np.random.uniform(-0.05, 0.05) * scale
            }

        # 2. MUSCULAR OVERLAY
        # Creating pull-vectors between bone anchors
        self.render_data["muscles"] = []
        muscle_groups = self.layers["L02"].groups
        for m_group, m_data in muscle_groups.items():
            anchors = m_data.get("anchors", [])
            if len(anchors) >= 2:
                # Find the 3D position of the start and end bones
                p1 = self.render_data["bones"].get(anchors[0])
                p2 = self.render_data["bones"].get(anchors[-1])
                
                if p1 and p2:
                    self.render_data["muscles"].append({
                        "id": m_group,
                        "p1": [p1["x"], p1["y"], p1["z"]],
                        "p2": [p2["x"], p2["y"], p2["z"]],
                        "tension": self.layers["L02"].activation_states[m_data["muscles"][0]]["tension"]
                    })

    def execute_biological_heartbeat(self):
        """Standard System Pulse"""
        # A. Process Growth
        if self.growth:
            self.growth.trigger_growth_tick()
            
        # B. Cognitive Processing (ADHD/Autism k=0.05)
        r = self.layers["L10"].get_resistance_matrix()
        self.layers["L00"].calculate_coherence(r, 0.01)
        
        # C. Visceral Demand (Square-Cube Penalty)
        # Moving a larger mass costs more ATP
        muscle_load = self.layers["L02"].calculate_metabolic_drain()
        self.layers["L05"].process_cycle(cognitive_load=0.1, muscle_strain=muscle_load)
        
        # D. Visual Synthesis
        self.synthesize_3d_body()
        
        return self.get_state()

    def get_state(self):
        return {
            "vitals": self.layers["L05"].get_vitals(),
            "growth": self.growth.get_growth_telemetry() if self.growth else {},
            "physics": self.render_data,
            "governance": self.layers["L00"].get_telemetry()
        }

