
# A7DO Sentience OS - Master Entity Frame (Maturation Assembler)
# Logic: Dynamic 3D Synthesis based on Developmental Ratios.

import numpy as np

class A7DO_Frame:
    def __init__(self, layers):
        self.layers = layers
        self.growth = layers.get("L07")
        self.physics_buffer = {"bones": {}, "muscles": []}

    def synthesize_3d_morphology(self):
        """Assembles the 206-bone skeleton using developmental proportions."""
        if not self.growth: return
        
        stats = self.growth.get_scaling_physics()
        x = stats["height"]
        head_r = stats["head_ratio"]
        limb_s = stats["limb_scalar"]
        
        bone_registry = self.layers["L01"].bone_registry
        self.physics_buffer["bones"] = {}

        for b_id, b_data in bone_registry.items():
            b_class = b_data.get("class", "GENERAL")
            side = 1.0 if "_R" in b_id else -1.0 if "_L" in b_id else 0.0
            
            # --- DEVELOPMENTAL PLACEMENT ---
            # Head (C3) stays at the top but occupies more/less % of height
            if b_class == "SKULL":
                y = x * (1.0 - (head_r / 2))
                x_off = side * 0.05 * x
            elif b_class == "SPINE":
                y = np.random.uniform(0.4, 1.0 - head_r) * x
                x_off = 0.0
            elif b_class == "UPPER":
                y = (1.0 - head_r - 0.1) * x
                x_off = side * 0.3 * x * limb_s
            elif b_class == "LOWER":
                y = np.random.uniform(0.1, 0.4) * x
                x_off = side * 0.15 * x * limb_s
            else:
                y = 0.5 * x
                x_off = side * 0.1 * x

            self.physics_buffer["bones"][b_id] = [x_off, y, np.random.uniform(-0.02, 0.02) * x]

        # --- MUSCULAR STRINGING ---
        self.physics_buffer["muscles"] = []
        for g_id, m_data in self.layers["L02"].groups.items():
            anchors = m_data.get("anchors", [])
            if len(anchors) >= 2:
                p1 = self.physics_buffer["bones"].get(anchors[0])
                p2 = self.physics_buffer["bones"].get(anchors[-1])
                if p1 and p2:
                    self.physics_buffer["muscles"].append({"p1": p1, "p2": p2})

    def execute_biological_heartbeat(self):
        """The Master Growth & Cognition Pulse."""
        if self.growth: self.growth.update_maturation()
        
        # Cognitive Resistance (k=0.05)
        r = self.layers["L10"].get_resistance_matrix()
        self.layers["L00"].calculate_coherence(r, 0.01)
        
        # Metabolic Tax (Cubic Mass)
        stats = self.growth.get_scaling_physics()
        self.layers["L05"].process_cycle(cognitive_load=0.2, muscle_strain=stats["mass"])
        
        self.synthesize_3d_morphology()
        return self.get_state()

    def get_state(self):
        return {
            "vitals": self.layers["L05"].get_vitals(),
            "growth": self.growth.get_scaling_physics() if self.growth else {},
            "physics": self.physics_buffer,
            "governance": self.layers["L00"].get_telemetry(),
            "logs": self.growth.log_archive if self.growth else []
        }

