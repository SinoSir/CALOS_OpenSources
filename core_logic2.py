"""
Project CALOS: Constant Altitude Levitation Over Sea
Core Control Logic v0.1 Alpha (Phased Release)
Founder: Liang Zhenxiong (梁振雄) | Date: 23 March 2026
"""

import time

class CALOSControlSystem:
    def __init__(self, max_design_load_ton: float):
        # 1.3x Redundancy Factor (The Liang Standard)
        self.phi = 1.3
        self.max_load = max_design_load_ton
        
        # Operational Safety Boundary: 1.3x stronger than maximum design load
        self.safe_capacity = self.max_load * self.phi
        
        # 12-bit Binary Mass Array (Counterweight System)
        # We divide the safe capacity into 2^12 (4096) units
        self.lsb_weight = self.safe_capacity / (2**12 - 1)
        
        print(f"--- CALOS System Initialized ---")
        print(f"Max Design Load: {self.max_load} Tons")
        print(f"1.3x Safety Boundary (Phi): {self.safe_capacity:.2f} Tons")
        print(f"12-bit Resolution (LSB): {self.lsb_weight * 1000:.2f} kg\n")

    def calculate_binary_weights(self, real_time_load: float):
        """
        Translates real-time sensor load into a 12-bit binary switching command.
        """
        # Safety Check: If load exceeds 1.3x, trigger Emergency Lock-out
        if real_time_load > self.safe_capacity:
            return "EMERGENCY_LOCKOUT", None
        
        # Calculate the number of units needed to offset the load
        units_needed = round(real_time_load / self.lsb_weight)
        
        # Binary Representation (12-bit)
        binary_command = format(units_needed, '012b')
        
        return "STABLE", binary_command

    def monitor_vital_signs(self, load: float, sea_state: int):
        """
        TCM-Inspired Structural Health Monitoring (Shan Le Sheng Logic).
        'Vital Signs' analysis for the bridge body.
        """
        status, command = self.calculate_binary_weights(load)
        
        print(f"[Sensor] Current Load: {load} Tons | Sea State: Level {sea_state}")
        
        if status == "EMERGENCY_LOCKOUT":
            print("⚠️ WARNING: Load exceeds 1.3x redundancy! Activating Structural Lock.")
        else:
            # Analyze 'Pulse' (Latency and Precision)
            precision = 1 - (abs(load - (int(command, 2) * self.lsb_weight)) / load) if load > 0 else 1.0
            print(f"[Actuator] Binary Switch Command: {command}")
            print(f"[Health] System Pulse Precision: {precision:.4%}")
        
        print("-" * 40)

# --- Quick Test (Simulation) ---
if __name__ == "__main__":
    # Example: A module designed for 1000 Tons
    calos = CALOSControlSystem(max_design_load_ton=1000)

    # Simulation 1: Standard Load (800 Tons)
    calos.monitor_vital_signs(800, sea_state=3)
    
    # Simulation 2: Heavy Load at Warning Boundary (1250 Tons)
    calos.monitor_vital_signs(1250, sea_state=5)
    
    # Simulation 3: Extreme Environment (1350 Tons - Exceeding 1.3x)
    calos.monitor_vital_signs(1350, sea_state=18)
