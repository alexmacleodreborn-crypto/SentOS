
# A7DO Sentience OS - Layer 01: Physical Architecture (Individual Bone Registry)
# Implementation: Absolute Physics Sandbox & Medical Simulation requirements.
# Regulation: Square-Cube Law (Height=x, Strength/Area=x^2, Mass/Volume=x^3)

class HumanChassis:
    """
    The High-Resolution Skeletal Chassis.
    Every bone is an individual object with unique physical properties 
    regulated by the user's Square-Cube scaling work.
    """
    def __init__(self, scale_x=1.0):
        self.scale_x = scale_x
        
        # SKELETAL REGISTRY (206 INDIVIDUAL NODES)
        # Structure: { ID: {"name": str, "type": str, "base_length_cm": float, "base_mass_g": float} }
        self.bone_registry = self._initialize_206_bones()

        # 32-TOOTH REGISTRY
        self.dental_manifold = {
            "Upper": [f"U_TOOTH_{i}" for i in range(1, 17)],
            "Lower": [f"L_TOOTH_{i}" for i in range(1, 17)]
        }

    def _initialize_206_bones(self):
        """Initializes baseline measurements for all 206 bones."""
        data = {}
        
        # --- AXIAL SKELETON (80 BONES) ---
        # Skull & Face (22)
        cranial = ["Frontal", "Parietal_L", "Parietal_R", "Temporal_L", "Temporal_R", "Occipital", "Sphenoid", "Ethmoid"]
        facial = ["Mandible", "Maxilla_L", "Maxilla_R", "Zygomatic_L", "Zygomatic_R", "Nasal_L", "Nasal_R", 
                  "Palatine_L", "Palatine_R", "Lacrimal_L", "Lacrimal_R", "Vomer", "Inf_Concha_L", "Inf_Concha_R"]
        for b in cranial + facial:
            data[b] = {"name": b, "class": "SKULL", "base_len": 5.0, "base_mass": 150.0}

        # Spine (26)
        vertebrae = [f"Cervical_{i}" for i in range(1, 8)] + [f"Thoracic_{i}" for i in range(1, 13)] + \
                    [f"Lumbar_{i}" for i in range(1, 6)] + ["Sacrum", "Coccyx"]
        for v in vertebrae:
            data[v] = {"name": v, "class": "SPINE", "base_len": 2.5, "base_mass": 40.0}

        # Thorax (25)
        thorax = ["Sternum_Manubrium", "Sternum_Body", "Xiphoid"] + [f"Rib_L_{i}" for i in range(1, 13)] + [f"Rib_R_{i}" for i in range(1, 13)]
        for t in thorax:
            data[t] = {"name": t, "class": "THORAX", "base_len": 15.0, "base_mass": 80.0}

        # Auditory & Hyoid (7)
        ear = ["Malleus_L", "Malleus_R", "Incus_L", "Incus_R", "Stapes_L", "Stapes_R", "Hyoid"]
        for e in ear:
            data[e] = {"name": e, "class": "SENSORY", "base_len": 0.5, "base_mass": 1.0}

        # --- APPENDICULAR SKELETON (126 BONES) ---
        # Upper Limbs (64)
        arms = ["Humerus_L", "Humerus_R", "Radius_L", "Radius_R", "Ulna_L", "Ulna_R", "Scapula_L", "Scapula_R", "Clavicle_L", "Clavicle_R"]
        hands = [f"Carpal_{s}_{i}" for s in ["L", "R"] for i in range(1, 9)] + \
                [f"Metacarpal_{s}_{i}" for s in ["L", "R"] for i in range(1, 6)] + \
                [f"Phalanx_H_{s}_{i}" for s in ["L", "R"] for i in range(1, 15)]
        for a in arms + hands:
            data[a] = {"name": a, "class": "UPPER", "base_len": 30.0 if "Humerus" in a else 5.0, "base_mass": 400.0 if "Humerus" in a else 10.0}

        # Lower Limbs (62)
        legs = ["Femur_L", "Femur_R", "Tibia_L", "Tibia_R", "Fibula_L", "Fibula_R", "Patella_L", "Patella_R", "Hip_L", "Hip_R"]
        feet = [f"Tarsal_{s}_{i}" for s in ["L", "R"] for i in range(1, 8)] + \
               [f"Metatarsal_{s}_{i}" for s in ["L", "R"] for i in range(1, 6)] + \
               [f"Phalanx_F_{s}_{i}" for s in ["L", "R"] for i in range(1, 15)]
        for l in legs + feet:
            data[l] = {"name": l, "class": "LOWER", "base_len": 45.0 if "Femur" in l else 4.0, "base_mass": 800.0 if "Femur" in l else 15.0}

        return data

    def get_regulated_bone_stats(self, bone_id):
        """
        Calculates individual bone stats using the Square-Cube Law.
        Returns the physics-corrected dimensions for the sandbox.
        """
        if bone_id not in self.bone_registry:
            return None
        
        base = self.bone_registry[bone_id]
        x = self.scale_x
        
        return {
            "id": bone_id,
            "length_cm": round(base["base_len"] * x, 2),        # x
            "strength_coeff": round(x ** 2, 2),                 # x^2
            "mass_g": round(base["base_mass"] * (x ** 3), 2),    # x^3
            "integrity": 1.0 # Placeholder for fracture modeling
        }

    def get_regulated_growth_metrics(self):
        """Total chassis metrics according to Square-Cube Law."""
        x = self.scale_x
        return {
            "height_scalar": round(x, 2),
            "global_strength": round(x ** 2, 2),
            "global_mass_volume": round(x ** 3, 2)
        }

    def verify_integrity(self):
        """Verification handshake for the Executive Dashboard."""
        active_bones = len(self.bone_registry)
        active_teeth = sum(len(arch) for arch in self.dental_manifold.values())
        
        return {
            "node_count": active_bones + active_teeth,
            "bones_status": "LOCKED" if active_bones == 206 else f"DESYNC_{active_bones}",
            "teeth_status": "LOCKED" if active_teeth == 32 else "ERROR",
            "manifold_geometry": "VITRUVIAN_HIGH_RES"
        }

    def get_bone_registry_by_class(self, class_name):
        """Returns IDs for a specific class (e.g., SPINE, SKULL)."""
        return [k for k, v in self.bone_registry.items() if v["class"] == class_name]

