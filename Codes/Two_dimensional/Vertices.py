"""
Parent static class Vertices:
    Contains methods for vertices and spline manipulations

    Attributes:
        verts               stores all vertices in the ready for BlockMesh form

        vert_count          counts how many vertices were created. Required for giving vertices ID

    Methods:
        get_airfoil_data    extracts coordinates from airfoil files.
                            saves top, bot, left, and right splines to an instance of a child class.
                            saves top_left, bot_left, bot_right, and top_right vertices to an instance of a child class.

        save_verts          takes a list of vertices and adds them to self.verts of an instance of a child class,
                            adds new IDs to self.verts_id of an instance of a child class,
                            saves vertices to Vertices.verts, and increments Vertices.vert_count

        get_verts           exports all vertices to the BlockMesh

        get_splines         exports all splines from self.b_splines and self.arc_splines of an instance
                            of a child class in the ready for BlockMesh form,
                            using static methods b_spline() and arc_spline()

        b_spline,           static methods, which take IDs of points and splines
        arc_spline          convert them to the ready for BlockMesh form
"""
import os


class Vertices:
    verts = []
    vert_count = 0

    def get_airfoil_data(self, airfoil_number):
        # Declaration of variables
        coord = []
        index = []
        top = []
        bot = []

        # Searching for airfoil files
        for line in open(os.path.abspath(f'../Coordinates/airfoil{airfoil_number}'), "r"):
            # Assign Coordinates
            if line.startswith('v'):
                coord.append((round(float(line.split()[1]), 4),
                              round(float(line.split()[2]), 4),
                              round(-1.0 * float(line.split()[3]), 4)))
            # Assign Indices
            elif line.startswith('l'):
                index.append((int(line.split()[1]) - 1, int(line.split()[2]) - 1))

        # Finding most left and right points
        most_right = (1000, 0, 0)
        most_left = (-1000, 0, 0)
        for line in coord:
            if line[0] < most_right[0]:
                most_right = line
            if line[0] > most_left[0]:
                most_left = line

        # Finding upper point from MostRight
        for line in index:
            if coord[line[0]] == most_right:
                if coord[line[1]][1] > most_right[1]:
                    previous_point = most_right
                    current_point = coord[line[1]]
                    break
            if coord[line[1]] == most_right:
                if coord[line[0]][1] > most_right[1]:
                    previous_point = most_right
                    current_point = coord[line[0]]
                    break

        # Assign coordinates to Top and Bot
        on_top = True
        while True:
            if on_top:
                top.append(current_point)
            for line in index:
                if coord[line[0]] == current_point:
                    if coord[line[1]] != previous_point:
                        previous_point = current_point
                        current_point = coord[line[1]]
                        break
                if coord[line[1]] == current_point:
                    if coord[line[0]] != previous_point:
                        previous_point = current_point
                        current_point = coord[line[0]]
                        break
            if current_point == most_right:
                break
            if not on_top:
                bot.append(current_point)
            elif current_point == most_left:
                on_top = False

        # Calculate Center point for the front circle
        boundary_right = [most_right[0] + 0.1 *
                          (most_left[0] - most_right[0]),
                          (most_left[1] + most_right[1]) / 2,
                          (most_left[2] + most_right[2]) / 2]

        boundary_left = [most_right[0] + 0.95 *
                         (most_left[0] - most_right[0]),
                         (most_left[1] + most_right[1]) / 2,
                         (most_left[2] + most_right[2]) / 2]

        # Finding boundary points
        delta = 1000
        for line in top:
            if delta > abs(boundary_right[0] - line[0]):
                top_right = line
                delta = abs(boundary_right[0] - line[0])
        delta = 1000
        for line in bot:
            if delta > abs(boundary_right[0] - line[0]):
                bot_right = line
                delta = abs(boundary_right[0] - line[0])
        delta = 1000
        for line in top:
            if delta > abs(boundary_left[0] - line[0]):
                top_left = line
                delta = abs(boundary_left[0] - line[0])
        delta = 1000
        for line in bot:
            if delta > abs(boundary_left[0] - line[0]):
                bot_left = line
                delta = abs(boundary_left[0] - line[0])

        # Brining back most_left and most_right points
        top.append(most_left)
        bot.append(most_right)

        # Dividing top and bot to bot_right/bot_left/top_right/top_left
        for line in bot:
            if line[0] < bot_right[0]:
                self.right.append(line)
            elif bot_left[0] > line[0] > bot_right[0]:
                self.bot.append(line)

        for line in top:
            if line[0] > top_left[0]:
                self.left.append(line)

        for line in top:
            if line[0] < top_right[0]:
                self.right.append(line)
            elif top_left[0] > line[0] > top_right[0]:
                self.top.append(line)

        for line in bot:
            if line[0] > bot_left[0]:
                self.left.append(line)

        # Saves vertices to verts and IDs to verts_id
        verts = [top_right, bot_right, bot_left, top_left]
        Vertices.save_verts(self, verts)

    def save_verts(self, verts):
        self.verts.extend(verts)
        Vertices.verts.extend(Vertices.get_verts(verts))
        self.verts_id.extend(list(range(Vertices.vert_count, Vertices.vert_count + len(verts))))
        Vertices.vert_count += len(verts)

    @staticmethod
    def get_verts(verts):
        output = []
        for i in range(len(verts)):
            output.append(f"\n\t({round(verts[i][0], 4)}   \t{round(verts[i][1], 4)}   "
                          f"\t{round(verts[i][2], 4)})\t\t//{Vertices.vert_count + i}")
        return output

    def get_splines(self):
        output = []
        for spline in self.b_splines:
            output.extend(Vertices.b_spline(spline[0], spline[1], spline[2]))
        for spline in self.arc_splines:
            output.extend(Vertices.arc_spline(spline[0], spline[1], spline[2]))
        return output

    @staticmethod
    def b_spline(v1, v2, verts):
        output = [f"\n\tBSpline {v1} {v2}",
                  "\n\t("]
        for vert in verts:
            output.append(f"\n\t\t({vert[0]} {vert[1]} {vert[2]})")
        output.append("\n\t)")
        return output

    @staticmethod
    def arc_spline(v1, v2, vert):
        return f"\narc {v1} {v2} ({vert[0]} {vert[1]} {vert[2]})"
