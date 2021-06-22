"""
class Splines:
    splines                     global list of all splines

    set_splines()               extracts b_splines and arc_splines from a local lists and
                                saves them in to the correct form to the global list

    b_spline()                  converts b_splines to the correct form

    arc_spline()                converts arc_splines to the correct form

    get_splines()               exports splines in the correct form from the global list of splines
"""


class Splines:
    splines = []

    @staticmethod
    def set_splines(profile):
        b_splines = profile.b_splines
        arc_splines = profile.arc_splines
        output = []
        for spline in b_splines:
            output.extend(Splines.b_spline(spline[0], spline[1], spline[2]))
        for spline in arc_splines:
            output.extend(Splines.arc_spline(spline[0], spline[1], spline[2]))
        Splines.splines.extend(output)

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

    @staticmethod
    def get_splines():
        return Splines.splines
