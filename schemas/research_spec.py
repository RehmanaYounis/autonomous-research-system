from typing import Optional

from pydantic import BaseModel, Field


class ResearchSpec(BaseModel):
    research_question: str = Field(
        description="The main research question or problem."
    )

    domain: str = Field(
        description="The research domain."
    )

    objective: str = Field(
        description="What the researcher wants to investigate or improve."
    )

    experiment_type: Optional[str] = Field(
        default=None,
        description="Simulation, physical, both, or not applicable."
    )

    existing_resources: list[str] = Field(
        default_factory=list,
        description="Existing papers, datasets, GitHub repositories, code, or other resources."
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Constraints specified by the researcher."
    )

    unknowns: list[str] = Field(
        default_factory=list,
        description="Important information still required before research can proceed."
    )
    
if __name__ == "__main__":
    spec = ResearchSpec(
        research_question="How can RL improve robotic grasping of unseen objects?",
        domain="reinforcement learning and robotics",
        objective="Improve generalization to unseen objects",
        experiment_type="simulation",
        existing_resources=["GitHub repository", "3 papers"],
        unknowns=["robot type", "simulation environment"],
    )

    print(spec.model_dump_json(indent=2))