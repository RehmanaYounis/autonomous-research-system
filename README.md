# Research Copilot

Research Copilot turns a research idea into a structured specification that can guide later research modules. The project is being built in modules; **Module 1, Requirements Agent, is implemented**. Literature Agent is the next module.

## Research flow

```text
Research idea
	|
	v
RequirementsAgent
	|-- analyze()       Create the initial ResearchSpec
	|-- next_question() Decide whether a required clarification is missing
	|-- update()        Incorporate the researcher's answer
	|-- run()           Repeat clarification for a bounded number of turns (5 in our case)
	|
	v
Final ResearchSpec
	|
	v
[Next module: Literature Agent]
```

The agent asks one question at a time and only asks for researcher-specific information that could materially affect the research direction or experimental setup. It should not ask the researcher to choose papers, algorithms, or methods that the system can investigate. The clarification loop allows up to five turns by default and returns the current specification when it finishes or reaches that limit.

## Modules and responsibilities

| Module or component | Responsibility | Status |
| --- | --- | --- |
| `RequirementsAgent` | Analyze the initial idea, identify important unknowns, decide whether clarification is needed, incorporate answers, and return a `ResearchSpec`. | Implemented (Module 1) |
| `ResearchSpec` | Shared structured state for the research question, domain, objective, experiment type, existing resources, constraints, requirements, and unresolved unknowns. | Implemented |
| Model providers | Provide a common `generate()` interface; `DeepSeekProvider` implements text and schema-validated structured responses using DeepSeek. | Implemented |
| `ModelRouter` | Select between configured cheap and strong model providers. | Implemented, not yet used by the requirements workflow |
| `LiteratureAgent` | Next module: use the finalized specification to discover and assess relevant literature. | Planned; placeholder only |
| Paper schema and literature search tool | Support structured paper data and literature discovery for the next module. | Planned; placeholders only |

## Module 1: Requirements Agent

The agent keeps the current `ResearchSpec` as its state. `analyze()` creates the first specification from the researcher's idea. If the specification has unknowns, `next_question()` asks the model whether any missing information must be clarified before research proceeds. `update()` applies the researcher's response while preserving known information and removing answered unknowns. `run()` coordinates these steps interactively and returns the final specification.

The specification distinguishes between `requirements` (scope or research-specific conditions to preserve) and `unknowns` (information the researcher still needs to provide). Information the system can investigate itself, such as which method is best, should not be treated as a researcher clarification.

## Run Module 1

This project requires Python 3.12 or newer and uses `uv` for its environment and dependencies. Set the DeepSeek API key in the environment before starting the interactive agent:

```bash
export DEEPSEEK_API_KEY="your-api-key"
uv sync
uv run python -m agents.requirements_agent
```

The script prompts for clarification when needed and prints the resulting `ResearchSpec` as JSON. The current workflow does not save the specification to `outputs/` or orchestrate later modules; those are not implemented yet.

## Project structure

```text
agents/       Research agents
models/       Model provider interface, DeepSeek provider, and model router
schemas/      Structured research and paper data models
tools/        Tools used by research modules, including planned literature search
outputs/      Reserved for generated research artifacts
```
