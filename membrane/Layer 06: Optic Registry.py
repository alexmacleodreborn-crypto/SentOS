
# A7DO Sentience OS - Layer 06: Optic Registry
# Perceptual Discovery Loop

import random

class OpticRegistry:
    def __init__(self):
        self.active_ingress = []
        self.discovery_flag = False
        self.target_mesh = None

    def scan_room(self, known_tokens):
        """ Simulates vision ingress tracking """
        meshes = ["MESH_USER", "MESH_CHASSIS", f"MESH_UNK_{random.randint(10,99)}"]
        self.active_ingress = []
        self.discovery_flag = False
        
        for m in meshes:
            # Check if this mesh ID is mapped to a linguistic token in L10
            is_known = any(node["token"] in m for node in known_tokens)
            self.active_ingress.append({"id": m, "known": is_known})
            if not is_known:
                self.discovery_flag = True
                self.target_mesh = m
        
        return self.active_ingress

