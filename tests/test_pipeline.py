import pytest
import json
import os
from pathlib import Path

# Add project root to path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import Orchestrator

def test_mumbai_pipeline():
    """Test the end-to-end pipeline with Mumbai case study"""
    orchestrator = Orchestrator()
    
    # Run the pipeline
    json_path, geom_path = orchestrator.run_case("data/inputs/mumbai_case.json")
    
    # Check that output files were created
    assert os.path.exists(json_path), f"JSON output file not found: {json_path}"
    assert os.path.exists(geom_path), f"Geometry output directory not found: {geom_path}"
    
    # Check that geometry file was created
    geom_file = os.path.join(geom_path, "mumbai_mass.obj")
    assert os.path.exists(geom_file), f"Geometry OBJ file not found: {geom_file}"
    
    # Check JSON structure
    with open(json_path, 'r') as f:
        result = json.load(f)
    
    # Verify required keys exist
    assert "case" in result
    assert "selected_rules" in result
    assert "calc" in result
    assert "rl" in result
    
    # Verify calculation results
    calc = result["calc"]
    assert "max_footprint_sqm" in calc
    assert "total_floor_area_sqm" in calc
    assert calc["max_footprint_sqm"] > 0
    assert calc["total_floor_area_sqm"] > 0
    
    # Verify RL results
    rl = result["rl"]
    assert "chosen_rule_path" in rl
    assert "rl_metrics" in rl

def test_pune_pipeline():
    """Test the end-to-end pipeline with Pune case study"""
    orchestrator = Orchestrator()
    
    # Run the pipeline
    json_path, geom_path = orchestrator.run_case("data/inputs/pune_case.json")
    
    # Check that output files were created
    assert os.path.exists(json_path), f"JSON output file not found: {json_path}"
    assert os.path.exists(geom_path), f"Geometry output directory not found: {geom_path}"
    
    # Check that geometry file was created
    geom_file = os.path.join(geom_path, "Pune_mass.obj")
    assert os.path.exists(geom_file), f"Geometry OBJ file not found: {geom_file}"
    
    # Check JSON structure
    with open(json_path, 'r') as f:
        result = json.load(f)
    
    # Verify required keys exist
    assert "case" in result
    assert "selected_rules" in result
    assert "calc" in result
    assert "rl" in result
    
    # Verify calculation results
    calc = result["calc"]
    assert "max_footprint_sqm" in calc
    assert "total_floor_area_sqm" in calc
    assert calc["max_footprint_sqm"] > 0
    assert calc["total_floor_area_sqm"] > 0
    
    # Verify RL results
    rl = result["rl"]
    assert "chosen_rule_path" in rl
    assert "rl_metrics" in rl

def test_output_directories():
    """Test that output directories are created correctly"""
    # Check that output directories exist
    assert os.path.exists("io/outputs/json"), "JSON output directory not found"
    assert os.path.exists("io/outputs/geometry"), "Geometry output directory not found"
    
    # Check that reports directory exists
    assert os.path.exists("reports"), "Reports directory not found"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])