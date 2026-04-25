
# A7DO Sentience OS - Layer 07: Morphological Sync (Developmental Edition)
# Logic: Human Maturation Ratios & Square-Cube Law
# Timeline: Neonatal -> Infant -> Toddler -> Child -> Adolescent -> Adult

import time

class GrowthEngine:
    """
    Manages the non-linear growth of the A7DO organism.
    Implements biological shifts in proportions (Head-to-Body Ratio).
    """
    def __init__(self, birth_scale=0.25):
        self.current_scale = birth_scale # Linear Height (x)
        self.maturity_index = 0.0        # 0.0 to 1.0
        
        # BIOLOGICAL STAGES (Age Approximation)
        self.stages = [
            {"name": "NEONATAL", "scale": 0.25, "head_ratio": 0.25, "limbs": 0.3},
            {"name": "INFANT", "scale": 0.35, "head_ratio": 0.22, "limbs": 0.4},
            {"name": "TODDLER", "scale": 0.50, "head_ratio": 0.20, "limbs": 0.5},
            {"name": "CHILD", "scale": 0.70, "head_ratio": 0.16, "limbs": 0.7},
            {"name": "ADOLESCENT", "scale": 0.85, "head_ratio": 0.14, "limbs": 0.9},
            {"name": "ADULT_SYNTHETIC", "scale": 1.0, "head_ratio": 0.125, "limbs": 1.0}
        ]
        
        self.log_archive = []

    def get_current_stage(self):
        """Returns the developmental stage based on current scale."""
        for stage in reversed(self.stages):
            if self.current_scale >= stage["scale"]:
                return stage
        return self.stages[0]

    def update_maturation(self, rate=0.002):
        """Processes the growth tick and logs morphological records."""
        if self.current_scale < 1.0:
            old_stage = self.get_current_stage()["name"]
            self.current_scale += rate
            new_stage = self.get_current_stage()["name"]
            
            if old_stage != new_stage:
                self.log_archive.append({
                    "timestamp": time.time(),
                    "event": f"MORPHOLOGICAL_SHIFT: {new_stage}",
                    "height": round(self.current_scale, 2)
                })
            return True
        return False

    def get_scaling_physics(self):
        """
        Calculates Square-Cube Law metrics.
        Height=x, Strength=x^2, Mass=x^3
        """
        x = self.current_scale
        stage = self.get_current_stage()
        return {
            "height": round(x, 4),
            "strength": round(x ** 2, 4),
            "mass": round(x ** 3, 4),
            "head_ratio": stage["head_ratio"],
            "limb_scalar": stage["limbs"],
            "stage_name": stage["name"]
        }

