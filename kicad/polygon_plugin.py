"""KiCad plugin to create polygon drawings (e.g. for edge cuts)."""

import math
import pcbnew


class PolygonPlugin(pcbnew.ActionPlugin):
    """Polygon plugin class."""

    N = 12  # number of edges - TODO get as user input
    LAYER_NAME = "Edge.Cuts"  # TODO get as user input
    RADIUS_MM = 50  # radius in mm - TODO get as user input

    def defaults(self):
        self.name = "RegularPolygon"
        self.category = "drawings"
        self.description = "A plugin to draw regular polygons."

    def Run(self):
        """Plugin run function."""
        board = pcbnew.GetBoard()

        radius = pcbnew.FromMM(self.RADIUS_MM)
        points = [(round(math.cos(2 * math.pi * i / self.N) * radius),
                   round(math.sin(2 * math.pi * i / self.N) * radius))
                  for i in range(self.N)]
        points_vector = pcbnew.wxPoint_Vector()
        for point in points:
            points_vector.append(pcbnew.wxPoint(point[0], point[1]))

        # draw polygon
        ds = pcbnew.DRAWSEGMENT(board)

        # ds.SetShape(pcbnew.S_SEGMENT)
        # ds.SetStart(pcbnew.wxPoint(0, 0))
        # ds.SetEnd(pcbnew.wxPoint(x, y))

        ds.SetShape(pcbnew.S_POLYGON)
        ds.SetPolyPoints(points_vector)

        # set layer
        layer_id = board.GetLayerID(self.LAYER_NAME)
        ds.SetLayer(layer_id)

        # TODO set line width if needed
        # ds.SetWidth(int(0.1 * pcbnew.IO_PER_MM))

        board.Add(ds)


PolygonPlugin().register()
