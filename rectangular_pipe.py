# -*- Hao with gpt4 -*-
import rhinoscriptsyntax as rs
import Rhino
import math

def make_rectangle_curve(frame, width, height, angle_rad):
    half_w = 0.5 * width
    half_h = 0.5 * height
    x_axis = frame.XAxis
    y_axis = frame.YAxis

    if abs(angle_rad) > 1e-9:
        rot = Rhino.Geometry.Transform.Rotation(angle_rad, frame.ZAxis, frame.Origin)
        x_axis.Transform(rot)
        y_axis.Transform(rot)

    pts = [
        frame.Origin + x_axis * half_w + y_axis * half_h,
        frame.Origin - x_axis * half_w + y_axis * half_h,
        frame.Origin - x_axis * half_w - y_axis * half_h,
        frame.Origin + x_axis * half_w - y_axis * half_h,
        frame.Origin + x_axis * half_w + y_axis * half_h
    ]

    return Rhino.Geometry.Polyline(pts).ToNurbsCurve()

def project_vector_to_plane(vector, plane):
    projection = vector - plane.ZAxis * (vector * plane.ZAxis)
    if projection.IsTiny():
        return None
    projection.Unitize()
    return projection

def compute_rotation_angle_in_plane(projected_vec, plane):
    x_comp = projected_vec * plane.XAxis
    y_comp = projected_vec * plane.YAxis
    return math.atan2(y_comp, x_comp)

def rectangular_pipe():
    rail_ids = rs.GetObjects("Select rail curve(s)", rs.filter.curve, preselect=True)
    if not rail_ids:
        print("No rails selected. Operation cancelled.")
        return

    width = rs.GetReal("Rectangle width (X-direction)", 10.0, minimum=0.01)
    if width is None:
        return
    height = rs.GetReal("Rectangle height (Y-direction)", 5.0, minimum=0.01)
    if height is None:
        return

    mode = rs.GetString("Choose rotation method", "Angle", ["Angle", "Vector"])
    if not mode:
        return

    use_fixed_angle = True
    fixed_angle_rad = 0.0
    world_reference_vector = None

    if mode == "Angle":
        angle_deg = rs.GetReal("Enter rotation angle (degrees, clockwise)", 0.0)
        if angle_deg is None:
            return
        fixed_angle_rad = math.radians(angle_deg)
    else:
        pts = rs.GetPoints("Pick two points to define direction vector (from → to)", max_points=2)
        if not pts or len(pts) != 2:
            print("Two points required for vector definition.")
            return
        vec = pts[1] - pts[0]
        if vec.IsTiny():
            print("Zero-length vector. Operation cancelled.")
            return
        vec.Unitize()
        world_reference_vector = vec
        use_fixed_angle = False

    doc = Rhino.RhinoDoc.ActiveDoc
    sweep = Rhino.Geometry.SweepOneRail()
    sweep.AngleToleranceRadians = doc.ModelAngleToleranceRadians
    sweep.ClosedSweep = True

    created_count = 0

    for rid in rail_ids:
        rail_obj = doc.Objects.Find(rid)
        if not rail_obj:
            continue
        rail = rail_obj.Geometry
        if not isinstance(rail, Rhino.Geometry.Curve):
            continue

        success, frame = rail.PerpendicularFrameAt(rail.Domain.T0)
        if not success:
            print("Could not compute frame on rail. Skipping.")
            continue

        if use_fixed_angle:
            angle_rad = fixed_angle_rad
        else:
            projected = project_vector_to_plane(world_reference_vector, frame)
            if not projected:
                print("Reference vector is parallel to rail normal. Skipping this rail.")
                continue
            angle_rad = compute_rotation_angle_in_plane(projected, frame)

        profile = make_rectangle_curve(frame, width, height, angle_rad)
        breps = sweep.PerformSweep(rail, profile)
        if not breps:
            print("Sweep failed on one rail.")
            continue

        for b in breps:
            doc.Objects.AddBrep(b)
            created_count += 1

    if created_count:
        doc.Views.Redraw()
        print("Created {} rectangular pipe(s).".format(created_count))
    else:
        print("No pipes were created.")

if __name__ == "__main__":
    rectangular_pipe()
