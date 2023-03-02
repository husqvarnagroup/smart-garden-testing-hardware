"""KiCad plugin to create polygon drawings (e.g. for edge cuts)."""

import math

import pcbnew


class PolygonPlugin(pcbnew.ActionPlugin):
    """Polygon plugin class."""

    # values for original 11-way power splitter:
    # - N = 12
    # - RADIUS_MM = 30
    # values for original 7-way power splitter with attenuators:
    # - N = 8
    # - RADIUS_MM = 25

    N = 8  # number of edges - TODO get as user input
    LAYER_NAME = "Edge.Cuts"  # TODO get as user input
    RADIUS_MM = 25  # radius in mm - TODO get as user input
    USE_POLYGON = False  # wether to use use segments or a polygon
    ADD_HOLES = True
    HOLE_DISTANCE_MM = 3  # distance to PCB corner
    HOLE_DIAMETER_MM = 2.5

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
            points_vector = pcbnew.VECTOR_VECTOR2I()
            for point in points:
                points_vector.append(pcbnew.VECTOR2I(point[0], point[1]))

            # draw polygon
            ds = pcbnew.PCB_SHAPE(board)
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
                ds = pcbnew.PCB_SHAPE(board)
                a = points[i]
                b = points[(i + 1) % self.N]
                ds.SetShape(pcbnew.S_SEGMENT)
                ds.SetStart(pcbnew.VECTOR2I(a[0], a[1]))
                ds.SetEnd(pcbnew.VECTOR2I(b[0], b[1]))
                ds.SetLayer(layer_id)
                board.Add(ds)

        if self.ADD_HOLES:
            hole_center_radius = pcbnew.FromMM(self.RADIUS_MM - self.HOLE_DISTANCE_MM)
            hole_points = [(round(math.cos(angle) * hole_center_radius),
                            round(math.sin(angle) * hole_center_radius))
                           for angle in angles]
            for i in range(self.N):
                circle = pcbnew.PCB_SHAPE(board)
                circle.SetShape(pcbnew.S_CIRCLE)
                circle.SetCenter(pcbnew.VECTOR2I(hole_points[i][0], hole_points[i][1]))
                circle.SetEnd(pcbnew.VECTOR2I(hole_points[i][0], hole_points[i][1] +
                                              pcbnew.FromMM(self.HOLE_DIAMETER_MM / 2)))
                circle.SetLayer(layer_id)
                board.Add(circle)


PolygonPlugin().register()
