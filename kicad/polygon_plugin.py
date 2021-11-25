"""KiCad plugin to create polygon drawings (e.g. for edge cuts)."""

import math
import pcbnew


class PolygonPlugin(pcbnew.ActionPlugin):
    """Polygon plugin class."""

    N = 12  # number of edges - TODO get as user input
    LAYER_NAME = "Edge.Cuts"  # TODO get as user input
    RADIUS_MM = 30  # radius in mm - TODO get as user input
    USE_POLYGON = False  # wether to use use segments or a polygon

    def defaults(self):
        """Properties for KiCad."""
        self.name = "RegularPolygon"
        self.category = "drawings"
        self.description = "A plugin to draw regular polygons."

    def Run(self):
        """Plugin run function."""
        board = pcbnew.GetBoard()

        radius = pcbnew.FromMM(self.RADIUS_MM)
        offset = 2 * math.pi / self.N / 2
        angles = [2 * math.pi * i / self.N + offset for i in range(self.N)]
        points = [(round(math.cos(angle) * radius),
                   round(math.sin(angle) * radius))
                  for angle in angles]

        layer_id = board.GetLayerID(self.LAYER_NAME)

        if self.USE_POLYGON:
            points_vector = pcbnew.wxPoint_Vector()
            for point in points:
                points_vector.append(pcbnew.wxPoint(point[0], point[1]))

            # draw polygon
            ds = pcbnew.DRAWSEGMENT(board)
            ds.SetShape(pcbnew.S_POLYGON)
            ds.SetPolyPoints(points_vector)

            # set layer
            ds.SetLayer(layer_id)

            # TODO set line width if needed
            # ds.SetWidth(int(0.1 * pcbnew.IO_PER_MM))

            board.Add(ds)

        else:
            for i in range(self.N):
                # draw polygon
                ds = pcbnew.DRAWSEGMENT(board)
                a = points[i]
                b = points[(i + 1) % self.N]
                ds.SetShape(pcbnew.S_SEGMENT)
                ds.SetStart(pcbnew.wxPoint(a[0], a[1]))
                ds.SetEnd(pcbnew.wxPoint(b[0], b[1]))
                ds.SetLayer(layer_id)
                board.Add(ds)


PolygonPlugin().register()
