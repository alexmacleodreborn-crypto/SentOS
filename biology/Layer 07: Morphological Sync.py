
# A7DO Sentience OS - Layer 07: Morphological Sync (Developmental Engine)
# Logic: Baby-to-Adult Synthetic Growth & Da Vinci Proportional Ratios
# Regulation: Square-Cube Law (x, x^2, x^3)

import time

class GrowthEngine:
    """
    Manages the non-linear biological growth of A7DO.
    Implements shifting proportions (Head-to-Body ratio) and scaling physics.
    """
    def __init__(self, birth_scale=0.2):
        self.current_scale = birth_scale # Height (x)
        self.maturity_index = 0.0
        
        # BIOLOGICAL DEVELOPMENT STAGES (Based on human proportions)
        self.stages = {
            "NEONATAL": {"min": 0.2, "head_ratio": 0.25, "limb_ratio": 0.3},
            "INFANT":   {"min": 0.3, "head_ratio": 0.22, "limb_ratio": 0.4},
            "TODDLER":  {"min": 0.45, "head_ratio": 0.20, "limb_ratio": 0.6},
            "CHILD":    {"min": 0.6, "head_ratio": 0.18, "limb_ratio": 0.8},
            "ADOLESCENT":{"min": 0.8, "head_ratio": 0.15, "limb_ratio": 0.9},
            "ADULT":    {"min": 1.0, "head_ratio": 0.125, "limb_ratio": 1.0}
        }
        
        self.developmental_log = []
        self.start_time = time.time()

    def get_current_stage(self):
        """Identifies current biological stage based on height scale."""
        current_stage = "NEONATAL"
        for stage, data in self.stages.items():
            if self.current_scale >= data["min"]:
                current_stage = stage
        return current_stage, self.stages[current_stage]

    def update_maturation(self, rate=0.001):
        """Processes the growth tick and logs milestones."""
        if self.current_scale < 1.0:
            old_stage, _ = self.get_current_stage()
            self.current_scale += rate
            new_stage, _ = self.get_current_stage()
            
            # Log milestone if stage changed
            if old_stage != new_stage:
                self.developmental_log.append({
                    "timestamp": time.time(),
                    "milestone": f"TRANSITION_TO_{new_stage}",
                    "height_cm": round(self.current_scale * 175, 1) # Estimated adult height 175cm
                })
            return True
        return False

    def get_scaling_physics(self):
        """
        Calculates Square-Cube Law metrics for Layer 05.
        """
        x = self.current_scale
        stage_name, stage_data = self.get_current_stage()
        
        return {
            "height_scalar": round(x, 4),
            "strength_area": round(x ** 2, 4),
            "mass_volume": round(x ** 3, 4),
            "head_to_body_ratio": stage_data["head_ratio"],
            "limb_development": stage_data["limb_ratio"],
            "stage": stage_name
        }

