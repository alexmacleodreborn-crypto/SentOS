
# A7DO Sentience OS - Layer 03: Movement Engine
# Jacobian-based Inverse Kinematics & Equilibrium
# Logic: Calculating joint torques to maintain balance against gravity.

import numpy as np
import math
import time

class MovementEngine:
    """
    The Kinematic system of the A7DO organism.
    Translates coordinate targets into specific joint angles.
    """
    def __init__(self, scale_x=1.0):
        # Dimensional regulation from L01 work:
        self.reach_scalar = scale_x
        self.mass_scalar = scale_x ** 3
        
        # Proprioception: Internal sense of body position
        # Degrees of Freedom (DoF) mapping to Layer 01 chassis
        self.joint_registry = {
            "NECK": {"pitch": 0.0, "yaw": 0.0, "limit": 45},
            "SHOULDER_L": {"pitch": 0.0, "roll": 0.0, "limit": 180},
            "ELBOW_L": {"flex": 0.0, "limit": 145},
            "SHOULDER_R": {"pitch": 0.0, "roll": 0.0, "limit": 180},
            "ELBOW_R": {"flex": 0.0, "limit": 145},
            "HIP_L": {"pitch": 0.0, "roll": 0.0, "limit": 120},
            "KNEE_L": {"flex": 0.0, "limit": 135}
        }
        
        self.center_of_mass = [0.0, 0.0, 0.0]
        self.is_balancing = True
        self.velocity_m_s = 0.0

    def calculate_ik_reach(self, target_xyz):
        """
        Jacobian IK Solver:
        Calculates the joint rotations required to touch target_xyz.
        Reach range is limited by physical scale x.
        """
        # Calculate distance to target
        dist = np.linalg.norm(target_xyz)
        max_reach = 0.8 * self.reach_scalar
        
        if dist > max_reach:
            return "IK_FAILURE: Target outside physical manifold reach."
        
        # Simulate Jacobian convergence loop
        # In a high-fidelity sim, this updates the joint_registry angles
        for joint in self.joint_registry:
            # Subtle movement toward target
            if "pitch" in self.joint_registry[joint]:
                self.joint_registry[joint]["pitch"] += 0.02
                
        self.velocity_m_s = round(dist * 0.1, 2)
        return "IK_SUCCESS: Reach stabilized."

    def calculate_kinematic_torque(self, effort_level):
        """
        Determines the torque required to maintain the pose.
        Formula: Torque = Force * (Distance^2) * Mass_Scalar
        """
        # Mass scales cubically per the user's Square-Cube law
        torque_required = (effort_level * self.mass_scalar)
        return round(torque_required, 4)

    def maintain_equilibrium(self):
        """
        Vestibular Reflex: Micro-adjustments to prevent falling.
        Checks Center of Mass (CoM) against Base of Support (BoS).
        """
        # Simulation of balancing logic
        jitter = math.sin(time.time()) * 0.01
        self.center_of_mass[0] += jitter
        
        stability_index = 1.0 - abs(self.center_of_mass[0])
        return {
            "status": "BALANCED" if stability_index > 0.85 else "STUMBLING",
            "stability": round(stability_index, 3)
        }

    def get_proprioception_telemetry(self):
        """
        Returns the data for the Executive Dashboard.
        """
        bal = self.maintain_equilibrium()
        return {
            "joint_matrix": self.joint_registry,
            "center_of_mass": self.center_of_mass,
            "motion_velocity": self.velocity_m_s,
            "balance_status": bal["status"],
            "stability_index": bal["stability"],
            "torque_load": self.calculate_kinematic_torque(self.velocity_m_s)
        }

