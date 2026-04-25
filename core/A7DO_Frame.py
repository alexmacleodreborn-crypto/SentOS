
# A7DO Sentience OS - Master Entity Frame (Biomechanical Synthesis)
# Logic: Hierarchical Assembly (Bones -> Joints -> Muscles)
# Regulation: Square-Cube Growth Scaling

import time
import numpy as np

class A7DO_Frame:
    """
    The High-Resolution Body Builder.
    Coordinates the maturation of the 206-bone chassis and 640-muscle system.
    """
    def __init__(self, layers):
        self.layers = layers
        self.growth = layers.get("L07")
        self.last_sync = time.time()
        
        # 3D Physical Manifold
        self.assembly = {
            "bones": {},       # 3D vertices [x, y, z]
            "muscles": [],      # Vector pairs [[x1,y1,z1], [x2,y2,z2]]
            "joints": {}        # Articulation points
        }

    def synthesize_biological_mesh(self):
        """
        Builds the body in the correct order based on Growth Scale (x).
        1. Skeletal frame placement.
        2. Muscular stringing across anchors.
        """
        x = self.growth.current_scale if self.growth else 1.0
        bone_registry = self.layers["L01"].bone_registry
        
        # A. SKELETAL SYNTHESIS (206 Nodes)
        self.assembly["bones"] = {}
        for b_id, b_data in bone_registry.items():
            b_class = b_data.get("class", "GENERAL")
            # Determine side for bilateral symmetry
            side = 1.0 if "_R" in b_id else -1.0 if "_L" in b_id else 0.0
            
            # Map vertical position based on Vitruvian centers
            y_base = 0.5
            if b_class == "SKULL": y_base = 0.9
            elif b_class == "SPINE": y_base = np.random.uniform(0.4, 0.8) # Spine column
            elif b_class == "UPPER": y_base = 0.7
            elif b_class == "LOWER": y_base = 0.3
            elif b_class == "FEET": y_base = 0.05
            
            # Scale coordinates by x (Linear Growth)
            self.assembly["bones"][b_id] = [
                side * np.random.uniform(0.05, 0.25) * x, # Width
                y_base * x,                               # Height
                np.random.uniform(-0.05, 0.05) * x        # Depth
            ]

        # B. MUSCULAR SYNTHESIS (640 Actuators)
        self.assembly["muscles"] = []
        muscle_groups = self.layers["L02"].groups
        for group_id, m_data in muscle_groups.items():
            anchors = m_data.get("anchors", [])
            if len(anchors) >= 2:
                p1 = self.assembly["bones"].get(anchors[0])
                p2 = self.assembly["bones"].get(anchors[-1])
                if p1 and p2:
                    self.assembly["muscles"].append({
                        "id": group_id,
                        "origin": p1,
                        "insertion": p2,
                        "tension": self.layers["L02"].activation_states[m_data["muscles"][0]]["tension"]
                    })

    def execute_biological_heartbeat(self):
        """
        The Master Execution Loop. 
        Ensures all layers are updated in the correct thermodynamic order.
        """
        # 1. Physical Growth (Maturation)
        if self.growth:
            self.growth.update_growth()
            
        # 2. Cognitive Calculation (k=0.05 ADHD/Autism profile)
        # Higher resistance R from associative jumps lowers coherence C
        res_r = self.layers["L10"].get_resistance_matrix()
        self.layers["L00"].calculate_coherence(res_r, 0.01)
        
        # 3. Visceral Metabolism (Square-Cube Cost)
        # Penalty is x^3 (mass) / x^2 (strength)
        mass_penalty = self.growth.mass_volume if self.growth else 1.0
        self.layers["L05"].process_cycle(cognitive_load=0.2, muscle_strain=mass_penalty)
        
        # 4. Physical 3D Assembly
        self.synthesize_biological_mesh()
        
        return self.get_unified_telemetry()

    def get_unified_telemetry(self):
        """Standardized data packet for the Dashboard."""
        return {
            "vitals": self.layers["L05"].get_vitals() if "L05" in self.layers else {"atp": 0, "bpm": 0},
            "growth": self.growth.get_telemetry() if self.growth else {"maturity_percent": 0},
            "physics": self.assembly,
            "governance": self.layers["L00"].get_telemetry() if "L00" in self.layers else {"coherence_index": 0}
        }

