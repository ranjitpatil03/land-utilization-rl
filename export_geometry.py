import os

def write_obj_box(path, width, depth, height):
    # Simple axis-aligned box with origin at (0,0,0)
    # 8 vertices, 12 triangles (using quads split into triangles)
    w, d, h = width, depth, height
    verts = [
        (0,0,0),(w,0,0),(w,d,0),(0,d,0),
        (0,0,h),(w,0,h),(w,d,h),(0,d,h)
    ]
    faces = [
        (1,2,3),(1,3,4), # bottom
        (5,6,7),(5,7,8), # top
        (1,5,6),(1,6,2), # side
        (2,6,7),(2,7,3),
        (3,7,8),(3,8,4),
        (4,8,5),(4,5,1)
    ]
    with open(path, "w", encoding="utf-8") as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for tri in faces:
            f.write(f"f {tri[0]} {tri[1]} {tri[2]}\n")

def export_from_results(out_dir, city, results):
    # derive a simple box:
    # width, depth from footprint (assume square), height from total floor area / footprint
    fp = max(results["max_footprint_sqm"], 1e-6)
    side = fp ** 0.5
    height = max(results["total_floor_area_sqm"] / fp, 3.0)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{city}_mass.obj")
    write_obj_box(out_path, side, side, height)
    return out_path
