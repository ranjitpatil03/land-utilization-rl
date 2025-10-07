import os

def write_obj_building(path, plot_width, plot_depth, building_width, building_depth, height, setback_front=0, setback_side=0):
    """
    Write a building with setbacks as an OBJ file.
    
    Args:
        path: Output file path
        plot_width: Total plot width
        plot_depth: Total plot depth
        building_width: Building footprint width
        building_depth: Building footprint depth
        height: Building height
        setback_front: Front setback distance
        setback_side: Side setback distance
    """
    # Calculate building position based on setbacks
    # Assuming front setback is applied to one side, side setback to both sides
    x_offset = setback_side
    y_offset = setback_front
    z_offset = 0  # Ground level
    
    # Building vertices (8 corners)
    verts = [
        # Bottom face (z = 0)
        (x_offset, y_offset, z_offset),  # 1: Front-left
        (x_offset + building_width, y_offset, z_offset),  # 2: Front-right
        (x_offset + building_width, y_offset + building_depth, z_offset),  # 3: Back-right
        (x_offset, y_offset + building_depth, z_offset),  # 4: Back-left
        # Top face (z = height)
        (x_offset, y_offset, z_offset + height),  # 5: Front-left-top
        (x_offset + building_width, y_offset, z_offset + height),  # 6: Front-right-top
        (x_offset + building_width, y_offset + building_depth, z_offset + height),  # 7: Back-right-top
        (x_offset, y_offset + building_depth, z_offset + height),  # 8: Back-left-top
    ]
    
    # Faces (triangles)
    faces = [
        # Bottom face
        (1, 2, 3), (1, 3, 4),
        # Top face
        (5, 6, 7), (5, 7, 8),
        # Front face
        (1, 5, 6), (1, 6, 2),
        # Back face
        (3, 7, 8), (3, 8, 4),
        # Left face
        (1, 4, 8), (1, 8, 5),
        # Right face
        (2, 6, 7), (2, 7, 3)
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        # Write vertices
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        # Write faces
        for tri in faces:
            f.write(f"f {tri[0]} {tri[1]} {tri[2]}\n")

def export_from_results(out_dir, city, results):
    """
    Export building geometry from calculation results.
    
    Args:
        out_dir: Output directory
        city: City name
        results: Calculation results dictionary
    """
    # Extract parameters from results
    plot_size = results["inputs"].get("plot_size", 500)
    setback = results.get("setback_m", 1.5)
    footprint = max(results["max_footprint_sqm"], 1e-6)
    
    # Calculate plot dimensions (assuming square plot)
    plot_side = plot_size ** 0.5
    plot_width = plot_side
    plot_depth = plot_side
    
    # Calculate building dimensions (considering setbacks)
    building_area = footprint
    # For simplicity, assuming square building footprint
    building_side = building_area ** 0.5
    building_width = min(building_side, plot_width - 2 * setback)
    building_depth = min(building_side, plot_depth - setback)  # Only front setback for depth
    
    # Calculate height from total floor area
    total_floor_area = max(results["total_floor_area_sqm"], 3.0)
    floors = max(total_floor_area / footprint, 1.0)
    floor_height = 3.0  # Standard floor height
    height = floors * floor_height
    
    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)
    
    # Use city name or default to "model" if not provided
    city_name = city if city else "model"
    out_path = os.path.join(out_dir, f"{city_name}_mass.obj")
    write_obj_building(out_path, plot_width, plot_depth, building_width, building_depth, height, setback, setback)
    return out_path