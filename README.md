# Land Utilization Optimization Pipeline

This project implements a multi-agent pipeline for optimizing land utilization based on regulatory rules using Reinforcement Learning.

## Repository Structure
```
project/
├── agents/                 # Individual agent implementations
├── data/
│   └── inputs/            # Sample input cases (Mumbai, Pune)
├── geometry/               # 3D geometry export utilities
├── io/
│   └── outputs/           # Output directory for results
├── land-utilization-rl/   # RL-specific components
├── outputs/               # Final outputs (JSON + geometry)
├── reports/               # Agent logs and reports
├── rl_env/                # Custom RL environment
├── rules_kb/              # Rule knowledge base
├── tests/                 # Unit and integration tests
├── utils/                 # Utility functions
├── README.md              # This file
├── handover.md            # Detailed handover documentation
├── config.py              # Configuration settings
└── requirements.txt       # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd project
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Pipeline

To run the pipeline with a specific case:

```bash
python agents/orchestrator.py data/inputs/mumbai_case.json
```

### Available Cases
- `data/inputs/mumbai_case.json` - Urban case study
- `data/inputs/pune_case.json` - Semi-urban case study

## Expected Outputs

After running the pipeline, you'll find the following outputs:

1. **JSON Reports**: Detailed analysis in `outputs/json/`
2. **Geometry Models**: 3D models in `outputs/geometry/` (OBJ format)
3. **Agent Logs**: Execution logs in `reports/agent_log.txt`
4. **RL Training Logs**: RL training metrics in `reports/rl_training_log.jsonl`

### Sample Console Output

When running the pipeline, you'll see detailed logging from each agent:

```
[00:52:04] Orchestrator: Starting run for case: data/inputs/mumbai_case.json
[00:52:04] InputAgent: Loading case from data\inputs\mumbai_case.json
[00:52:04] InputAgent: Successfully loaded case with keys: ['case_id', 'location', 'road_width', 'plot_size']
[00:52:04] Would download: https://example.com/regulations.pdf
[00:52:04] Parsing (stub): rules_kb/sample_rules.json
[00:52:04] Classification Agent: Starting to select applicable rules.
[00:52:04] Classification Agent: SELECTED rule R-SETBACK-URBAN
[00:52:04] Classification Agent: SELECTED rule R-COVERAGE
[00:52:04] Classification Agent: SELECTED rule R-FAR
[00:52:04] Classification Agent: Found 3 applicable rules.
[00:52:04] Classification Agent: Decision details - SELECTED rule R-SETBACK-URBAN: Condition match: location=urban, SELECTED rule R-COVERAGE: No conditions, SELECTED rule R-FAR: No conditions
[00:52:04] Calculation Agent: Starting computations.
[00:52:04] Calculation Agent: Processing case with plot size: 500 sqm
[00:52:04] Calculation Agent: Location is urban
[00:52:04] Calculation Agent: Evaluating setback for road width 9
[00:52:04] Calculation Agent: Using default setback value: 1.5
[00:52:04] Calculation Agent: Coverage for urban is 0.6
[00:52:04] Calculation Agent: FAR for urban is 1.8
[00:52:04] Calculation Agent: Max footprint: 300.0 sqm, Total floor area: 900.0 sqm
[00:52:04] Calculation Agent: Finished. Total floor area: 900.0 sqm.
[00:52:04] RL Agent: Starting RL decision process.
[00:52:04] RL Agent: Expected rule path: ['R-FAR', 'R-COVERAGE', 'R-SETBACK-URBAN']
[00:52:04] RL Agent: Candidate 1 (expected): ['R-FAR', 'R-COVERAGE', 'R-SETBACK-URBAN']
[00:52:04] RL Agent: Candidate 2 (reversed): ['R-SETBACK-URBAN', 'R-COVERAGE', 'R-FAR']
[00:52:04] RL Agent: Candidate 3 (rotated): ['R-COVERAGE', 'R-SETBACK-URBAN', 'R-FAR']
[00:52:04] RL Agent: Initializing RL environment and training...
[00:52:04] RL Environment: Initialized with 3 candidate paths
[00:52:04] Training RL (random policy) for 10 episodes...
[00:52:04] EP 1: action=0, reward=1, chosen=['R-FAR', 'R-COVERAGE', 'R-SETBACK-URBAN'] expected=['R-FAR', 'R-COVERAGE', 'R-SETBACK-URBAN']
...
[00:52:04] Avg reward: -0.60, Success rate: 20.00%
[00:52:04] RL Agent: Training complete. Metrics: {'avg_reward': -0.6, 'success_rate': 0.2, 'episodes': 10}
[00:52:04] RL Agent: Process complete.
[00:52:04] Orchestrator: Saved JSON report to io/outputs\json\mumbai_output.json
[00:52:04] Orchestrator: Saved geometry to io/outputs\geometry\mumbai_model.stl
[00:52:04] Orchestrator: Run complete.
```

## Running RL Training

To train the RL agent:

```bash
python land-utilization-rl/run_pipeline.py
```

## Adding New Rules

1. Edit `rules_kb/sample_rules.json` to add new rules
2. Rules follow a structured format with conditions and logic
3. Each rule should have a unique ID and clear description

## Testing

Run the test suite to verify the pipeline:

```bash
python -m pytest tests/ -v
```

## Known Limitations

1. Current implementation uses a simplified RL environment for demonstration
2. Rule parsing is basic and doesn't include metadata tagging (page numbers, clause numbers)
3. Geometry export is a simplified box model representation

## Advanced Features

### Structured Logging
The system now includes structured logging in JSONL format for better analysis:
- Agent execution logs: `reports/agent_log.txt`
- RL training metrics: `reports/rl_training_log.jsonl`

### Feedback Loop
The system supports user feedback integration:
- API endpoint for feedback submission
- RL reward integration for 👍 (+2) and 👎 (-2) feedback
- Simple UI for viewing outputs and providing feedback

### Enhanced Geometry Export
Geometry exports now include:
- Parametric blocks with setbacks
- Height visualization based on floor area
- OBJ format for compatibility with 3D software