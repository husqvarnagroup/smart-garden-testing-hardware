"""KiCad plugin to place parts for power splitter."""

import math
import pcbnew


class PowerSplitterPartsPlacementPlugin(pcbnew.ActionPlugin):
    """Power splitter parts placement plugin class."""

    N = 12
    RADIUS_R_MM = 5
    RADIUS_J_MM = 24.5

    def defaults(self):
        self.name = "PowerSplitterPartsPlacement"
        self.category = "drawings"
        self.description = "A plugin to place power splitter parts."

    def Run(self):
        """Plugin run function."""
        board = pcbnew.GetBoard()
        components = board.GetModules()

        connectors = []
        resistors = []
        for component in components:
            if component.GetReference().startswith("J"):
                connectors.append(component)
            if component.GetReference().startswith("R"):
                resistors.append(component)

        connectors.sort(key=lambda x: int(x.GetReference()[1:]))
        resistors.sort(key=lambda x: int(x.GetReference()[1:]))

        radius_r = pcbnew.FromMM(self.RADIUS_R_MM)
        radius_j = pcbnew.FromMM(self.RADIUS_J_MM)
        for i in range(self.N):
            angle = 2 * math.pi * i / self.N
            angle_deg = - 360 * i / self.N

            connectors[i].SetOrientationDegrees(angle_deg-90)
            resistors[i].SetOrientationDegrees(angle_deg)

            x = math.cos(angle)
            y = math.sin(angle)

            connectors[i].SetPosition(pcbnew.wxPoint(round(x * radius_j),
                                                     round(y * radius_j)))
            resistors[i].SetPosition(pcbnew.wxPoint(round(x * radius_r),
                                                    round(y * radius_r)))


PowerSplitterPartsPlacementPlugin().register()
