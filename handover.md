# Land Utilization Pipeline - Handover Document

## Repository Structure

```
project/
├── agents/                 # Individual agent implementations
│   ├── calc_agent.py       # Calculation agent for rule-based computations
│   ├── classify_agent.py   # Rule classification agent
│   ├── fetch_agent.py      # Document fetching agent
│   ├── input_agent.py      # Input processing agent
│   ├── orchestrator.py     # Main pipeline orchestrator
│   ├── parse_agent.py      # Document parsing agent
│   └── rl_agent.py         # Reinforcement learning agent
├── data/
│   └── inputs/            # Sample input cases (Mumbai, Pune)
├── geometry/               # 3D geometry export utilities
├── outputs/               # Final outputs (JSON + geometry)
├── reports/               # Agent logs and reports
├── rl_env/                 # Custom RL environment
├── rules_kb/               # Rule knowledge base
├── tests/                  # Unit and integration tests
├── utils/                  # Utility functions
├── feedback_api.py         # User feedback API endpoint
├── feedback_ui.html        # Simple feedback UI
├── README.md               # Project documentation
├── handover.md             # This document
├── config.py               # Configuration settings
└── requirements.txt        # Python dependencies
```

## How to Add New Rules/Documents

### Adding New Rules

1. Edit `rules_kb/enhanced_rules.json` to add new rules
2. Rules follow a structured format with metadata, conditions and logic:
   ```json
   {
     "id": "RULE-ID",
     "authority": "Governing Body",
     "clause": "Clause Number",
     "page": "Page Number",
     "description": "Rule description",
     "conditions": {
       "field": "value"
     },
     "logic": [
       {
         "if": {
           "condition": "value"
         },
         "result": "value"
       }
     ]
   }
   ```

3. Each rule should have:
   - A unique ID with authority prefix
   - Metadata (authority, clause, page)
   - Clear description
   - Appropriate conditions for applicability
   - Logic for computation or mapping

### Adding New Documents

1. Add PDF documents to the `rules_kb/` directory
2. Update the fetch agent (`agents/fetch_agent.py`) to include URLs for new documents
3. Update the parse agent (`agents/parse_agent.py`) to handle parsing of new document formats

## How to Run RL Training

The RL component uses a custom environment with feedback integration:

1. **Environment**: The RL environment (`rl_env/rule_path_env.py`) where:
   - State: Index in a list of candidate rule IDs
   - Actions: Choose one of candidate paths (index)
   - Reward: Base reward (+1 if chosen path matches expected, else -1) + Feedback reward (+2 for 👍, -2 for 👎)

2. **Training**: To train the RL agent:
   ```bash
   python agents/orchestrator.py data/inputs/mumbai_redevelopment.json
   ```

3. **Feedback Integration**: The system now integrates user feedback:
   - API endpoint at `/feedback` for submitting feedback
   - Positive feedback (👍) adds +2 to rewards
   - Negative feedback (👎) subtracts -2 from rewards
   - Rewards are loaded from `feedback.json` during RL training

## Known Limitations

1. **Simplified RL Environment**: The current RL implementation uses a toy environment with a random policy. For production use, this should be replaced with a proper PPO or other RL algorithm from Stable-Baselines3.

2. **Basic Rule Parsing**: Rule parsing is basic and doesn't include advanced metadata extraction.

3. **Enhanced Geometry Export**: Geometry export now includes setbacks and height visualization based on floor area calculations.

4. **Stub Document Fetching**: Document fetching is currently a stub that doesn't actually download documents.

5. **Expanded Test Coverage**: Test coverage has been expanded to include feedback system validation.

6. **Hardcoded Paths**: Some paths are hardcoded and should be made configurable.

## Multi-Agent Architecture

The pipeline uses a multi-agent architecture where each agent has a specific responsibility:

1. **Input Agent**: Loads and validates input cases
2. **Fetch Agent**: Retrieves regulatory documents (stub implementation)
3. **Parse Agent**: Parses documents into structured rules (stub implementation)
4. **Classify Agent**: Selects applicable rules based on case parameters
5. **Calc Agent**: Performs calculations based on selected rules
6. **RL Agent**: Uses reinforcement learning to optimize rule application order
7. **Orchestrator**: Coordinates the entire pipeline

## Outputs

The pipeline generates several types of outputs:

1. **JSON Reports**: Detailed analysis in `outputs/json/`
2. **Geometry Models**: 3D models in `outputs/geometry/` (OBJ format with setbacks and height)
3. **Agent Logs**: Execution logs in `reports/agent_log.txt`
4. **RL Training Logs**: Structured RL metrics in `reports/rl_training_log.jsonl`
5. **Feedback Data**: User feedback stored in `feedback.json`

## Case Studies

### Mumbai Redevelopment Case
- Input: `data/inputs/mumbai_redevelopment.json`
- Rules: Mumbai DCPR 2034, MCGM, MHADA
- Output: Enhanced FAR for slum redevelopment projects

### Ahmedabad Residential Case
- Input: `data/inputs/ahmedabad_residential.json`
- Rules: Ahmedabad DCR
- Output: Standard residential development analysis

## Feedback System

The system includes a complete feedback loop:

1. **API Endpoint**: Flask-based API at `/feedback`
2. **UI Interface**: Simple HTML interface for feedback submission
3. **Reward Integration**: Feedback directly influences RL training
4. **Statistics**: Feedback statistics tracking

## Next Steps for Production

1. **Implement Real RL Training**: Replace the random policy with actual PPO training using Stable-Baselines3
2. **Enhance Document Processing**: Implement real PDF parsing and metadata extraction
3. **Expand Test Coverage**: Add more comprehensive unit and integration tests
4. **Add Configuration Management**: Make paths and parameters configurable
5. **Implement Error Handling**: Add more robust error handling and recovery
6. **Performance Optimization**: Optimize performance for large rule sets
7. **Production Deployment**: Containerize the application for deployment
8. **Database Integration**: Store feedback and results in a proper database
9. **User Authentication**: Add authentication for the feedback system
10. **Advanced Visualization**: Implement more sophisticated 3D visualization