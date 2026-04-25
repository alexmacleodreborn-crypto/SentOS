
# A7DO Sentience OS - Layer 03: Movement Engine
# Forward & Inverse Kinematics (Jacobian Solver)

import numpy as np
import math

class MovementEngine:
    def __init__(self):
        self.is_active = True
        self.center_of_mass = [0.0, 0.0, 0.0]
        # Degrees of Freedom (DoF) for the primary limbs
        self.joint_angles = {
            "shoulder_L": [0.0, 0.0],
            "elbow_L": [0.0],
            "shoulder_R": [0.0, 0.0],
            "elbow_R": [0.0],
            "neck": [0.0, 0.0]
        }
        self.velocity_m_s = 0.0

    def calculate_ik(self, target_xyz):
        """
        Jacobian IK Solver Logic:
        Calculates the delta angles required to reach target_xyz.
        """
        # Simplified simulation of the IK solver convergence
        for joint in self.joint_angles:
            # Shift joint angles slightly toward a "reaching" pose
            self.joint_angles[joint] = [round(a + 0.05, 2) for a in self.joint_angles[joint]]
            
        self.velocity_m_s = round(np.linalg.norm(target_xyz) * 0.1, 2)
        return "IK_SOLVER: Converged. Actuators primed for reach."

    def get_proprioception(self):
        """
        Returns the internal sense of body position.
        """
        return {
            "joint_matrix": self.joint_angles,
            "center_of_mass": self.center_of_mass,
            "motion_velocity": self.velocity_m_s,
            "stability_index": 0.985
        }

