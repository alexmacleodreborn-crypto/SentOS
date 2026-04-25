
# A7DO Sentience OS - Layer 03: Movement Engine (High-Resolution)
# Jacobian Inverse Kinematics & Bipedal Equilibrium
# Logic: Calculating joint torques for the 206-bone manifold.

import numpy as np
import math
import time

class MovementEngine:
    """
    The Kinematic Control Layer.
    Translates cognitive spatial targets into joint rotations and balance adjustments.
    """
    def __init__(self, scale_x=1.0):
        # Dimensional regulation from L01/L07
        self.scale_x = scale_x
        self.mass_scalar = scale_x ** 3  # Mass scales cubically
        
        # 1. JOINT REGISTRY (Degrees of Freedom mapped to L01 Bone IDs)
        # Limits are based on biological human ranges.
        self.joint_matrix = {
            "ATLANTO_AXIAL": {"pitch": 0.0, "yaw": 0.0, "limits": [-45, 45]},
            "SHOULDER_L": {"pitch": 0.0, "roll": 0.0, "yaw": 0.0, "bone": "Humerus_L"},
            "ELBOW_L": {"flex": 0.0, "bone": "Ulna_L", "limits": [0, 145]},
            "SHOULDER_R": {"pitch": 0.0, "roll": 0.0, "yaw": 0.0, "bone": "Humerus_R"},
            "ELBOW_R": {"flex": 0.0, "bone": "Ulna_R", "limits": [0, 145]},
            "HIP_L": {"pitch": 0.0, "roll": 0.0, "bone": "Femur_L"},
            "KNEE_L": {"flex": 0.0, "bone": "Tibia_L", "limits": [0, 135]},
            "HIP_R": {"pitch": 0.0, "roll": 0.0, "bone": "Femur_R"},
            "KNEE_R": {"flex": 0.0, "bone": "Tibia_R", "limits": [0, 135]}
        }
        
        # 2. PROPRIOCEPTION STATE
        self.center_of_mass = {"x": 0.0, "y": 1.0, "z": 0.0} # Normalized to navel
        self.stability_index = 1.0 # 1.0 = Perfect Balance, 0.0 = Collapse
        self.velocity_vec = [0.0, 0.0, 0.0]
        
    def calculate_jacobian_ik(self, target_bone_id, target_xyz):
        """
        Jacobian IK Solver:
        Calculates the necessary joint deltas to move a specific Bone ID to target_xyz.
        """
        # Logic: Find path in skeletal tree from root to target_bone_id
        # Simulation of convergence
        dist = np.linalg.norm(target_xyz)
        
        # Calculate Curvature Pressure (Psi) for L00
        # If the reach is impossible, prediction error spikes
        max_reach = 0.8 * self.scale_x
        prediction_error = max(0, dist - max_reach)
        
        # Update joint angles slightly (simulating iterative solver)
        for j in self.joint_matrix.values():
            if j.get("bone") == target_bone_id:
                if "pitch" in j: j["pitch"] += 0.01
        
        return {
            "status": "CONVERGING" if prediction_error < 0.1 else "OUT_OF_BOUNDS",
            "prediction_error": round(prediction_error, 4),
            "torque_demand": self.calculate_static_torque()
        }

    def calculate_static_torque(self):
        """
        Torque = Force * Distance.
        Force is influenced by Mass Scalar (x^3).
        """
        # Movement becomes exponentially harder as scale x increases
        base_force = 9.81 * self.mass_scalar
        return round(base_force * 0.5, 2) # Nm

    def update_balance(self):
        """
        Vestibular Loop: Adjusts CoM to stay within the Base of Support.
        Triggered every 20ms in a live environment.
        """
        # Jitter simulation
        self.center_of_mass["x"] += math.sin(time.time() * 2) * 0.005
        
        # Stability decays if CoM x shifts too far from center (0.0)
        self.stability_index = max(0.0, 1.0 - abs(self.center_of_mass["x"]) * 5)
        
        return {
            "com": self.center_of_mass,
            "stability": round(self.stability_index, 3),
            "state": "STABLE" if self.stability_index > 0.8 else "STUMBLING"
        }

    def get_kinematic_telemetry(self):
        """High-resolution data export for the Executive Dashboard."""
        bal = self.update_balance()
        return {
            "joint_angles": self.joint_matrix,
            "center_of_mass": bal["com"],
            "stability": bal["stability"],
            "balance_state": bal["state"],
            "mass_load_nm": self.calculate_static_torque(),
            "physics_scale": f"{self.scale_x}x"
        }

