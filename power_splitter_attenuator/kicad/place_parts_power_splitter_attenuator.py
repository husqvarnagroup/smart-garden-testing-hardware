"""KiCad plugin to place parts for power splitter."""

import math

import pcbnew


class PowerSplitterAttenuatorPartsPlacementPlugin(pcbnew.ActionPlugin):
    """Power splitter parts placement plugin class."""

    N = 8
    # SMA connectors
    RADIUS_J_MM = 20.5  # experimentally determined to align with board edge
    # resistors for attenuators
    RADIUS_R1_MM = 16
    RADIUS_R2_MM = 14
    RADIUS_R3_MM = 12
    # resistors for power splitter
    RADIUS_R4_MM = 8
    # shift for resistors that are rotated by 90 degrees
    ROTATED_R_SHIFT_MM = 0.51  # experimentally determined; expected value from measurements is 0.525

    def defaults(self):
        """Define properties of plugin."""
        self.name = "PowerSplitterAttenuatorPartsPlacement"
        self.category = "drawings"
        self.description = "A plugin to place power splitter parts."

    def Run(self):
        """Plugin run function."""
        board = pcbnew.GetBoard()
        components = board.GetFootprints()

        connectors = []
        resistors = []
        for component in components:
            if component.GetReference().startswith("J"):
                connectors.append(component)
            if component.GetReference().startswith("R"):
                resistors.append(component)

        connectors.sort(key=lambda x: int(x.GetReference()[1:]))
        resistors.sort(key=lambda x: int(x.GetReference()[1:]))

        radius_j = pcbnew.FromMM(self.RADIUS_J_MM)
        radius_r1 = pcbnew.FromMM(self.RADIUS_R1_MM)
        radius_r2 = pcbnew.FromMM(self.RADIUS_R2_MM)
        radius_r3 = pcbnew.FromMM(self.RADIUS_R3_MM)
        radius_r4 = pcbnew.FromMM(self.RADIUS_R4_MM)

        for i in range(self.N):
            angle = 2 * math.pi * i / self.N
            angle_deg = - 360 * i / self.N

            x = math.cos(angle)
            y = math.sin(angle)

            # SMA connectors
            connectors[i].SetOrientationDegrees(angle_deg)
            connectors[i].SetPosition(pcbnew.VECTOR2I(round(x * radius_j),
                                                      round(y * radius_j)))

            # attenuator resistors
            resistors[4 * i].SetOrientationDegrees((angle_deg + 90) % 360)  # R1, R5, ..
            resistors[4 * i + 1].SetOrientationDegrees((angle_deg + 180) % 360)  # R2, R6, ..
            resistors[4 * i + 2].SetOrientationDegrees((angle_deg - 90) % 360)  # R3, R7, ..

            shift_x = pcbnew.FromMM(math.cos(angle + math.pi / 2) * self.ROTATED_R_SHIFT_MM)
            shift_y = pcbnew.FromMM(math.sin(angle + math.pi / 2) * self.ROTATED_R_SHIFT_MM)

            resistors[4 * i].SetPosition(pcbnew.VECTOR2I(round(x * radius_r1 + shift_x),
                                                         round(y * radius_r1 + shift_y)))
            resistors[4 * i + 1].SetPosition(pcbnew.VECTOR2I(round(x * radius_r2),
                                                             round(y * radius_r2)))
            resistors[4 * i + 2].SetPosition(pcbnew.VECTOR2I(round(x * radius_r3 + shift_x),
                                                             round(y * radius_r3 + shift_y)))

            # power slitter resistors (R4, R8, ..)
            resistors[4 * i + 3].SetOrientationDegrees((angle_deg + 180) % 360)
            resistors[4 * i + 3].SetPosition(pcbnew.VECTOR2I(round(x * radius_r4),
                                                             round(y * radius_r4)))


PowerSplitterAttenuatorPartsPlacementPlugin().register()
