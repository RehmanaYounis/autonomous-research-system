from models.base import BaseModelProvider
from schemas.research_spec import ResearchSpec


class RequirementsAgent:
    def __init__(self, model: BaseModelProvider):
        self.model = model
        self.research_spec: ResearchSpec | None = None

    def analyze(self, user_input: str) -> ResearchSpec:

        system_prompt = """
        You are a research requirements agent.

        Your goal is to understand the researcher's research problem
        and create a ResearchSpec.

        Rules:
        - Do not invent information.
        - Identify only information that is genuinely required before
          research can proceed.
        - Do not ask the researcher to choose things that the research
          system itself should investigate, such as which algorithm is best,
          which papers should be read, or which methods should be compared.
        - Put genuinely missing researcher-specific information in unknowns.
        - Preserve important research-specific scope or requirements in the
          requirements field.
        """

        prompt = f"""
        Researcher's input:

        {user_input}

        Create the research specification.
        """

        self.research_spec = self.model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            response_schema=ResearchSpec,
        )

        return self.research_spec
    
    def update(self, user_input: str) -> ResearchSpec:
        if self.research_spec is None:
            return self.analyze(user_input)

        system_prompt = """
        You are a research requirements agent.

        Update the existing ResearchSpec using the researcher's new information.

        Rules:
        - Preserve previously known information unless the researcher
        explicitly changes it.
        - Do not invent information.
        - Remove an item from unknowns when the researcher has answered it.
        - Add an unknown only when the researcher genuinely needs to provide
        that information before research can proceed.
        - Do not ask the researcher to make decisions that the research system
        itself should investigate.
        - When the researcher defines the scope of the problem, preserve that
        information in requirements rather than discarding or merely paraphrasing it.
        """

        prompt = f"""
        CURRENT RESEARCH SPEC:

        {self.research_spec.model_dump_json(indent=2)}

        NEW INFORMATION FROM RESEARCHER:

        {user_input}

        Update the ResearchSpec.
        """

        self.research_spec = self.model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            response_schema=ResearchSpec,
        )

        return self.research_spec
    
    def next_question(self) -> str | None:
        if self.research_spec is None:
            raise ValueError("No ResearchSpec exists yet.")

        if not self.research_spec.unknowns:
            return None

        system_prompt = """
        You are a research requirements agent.

        Your job is to decide whether the researcher must answer another
        clarification question before the research process can proceed.

        Important rules:
        - Do not ask for information the research system can investigate itself.
        - Do not ask which algorithm, paper, dataset, or method is best.
        - Do not ask optional questions merely because more detail would be useful.
        - Ask only when missing information would materially affect the research
        direction or experimental setup.
        - Ask only ONE question at a time.
        - If no clarification is necessary, return exactly: PROCEED
        """

        prompt = f"""
        CURRENT RESEARCH SPEC:

        {self.research_spec.model_dump_json(indent=2)}

        Decide whether another clarification from the researcher is required.

        If required, return the single most important question.
        Otherwise return exactly: PROCEED
        """

        response = self.model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )

        response = response.strip()

        if response.upper() == "PROCEED":
            return None

        return response
    
    
    def run(
    self,
    initial_input: str,
    max_clarification_turns: int = 5,
) -> ResearchSpec:

        self.analyze(initial_input)

        clarification_turns = 0

        while clarification_turns < max_clarification_turns:
            question = self.next_question()

            if question is None:
                break

            print(f"\nAgent: {question}")

            answer = input("Researcher: ")

            self.update(answer)

            clarification_turns += 1

        return self.research_spec

if __name__ == "__main__":
    from models.deepseek import DeepSeekProvider

    model = DeepSeekProvider()
    agent = RequirementsAgent(model)

    final_spec = agent.run(
        """
        I want to research how reinforcement learning can help
        a robotic arm learn to grasp previously unseen objects.
        """
    )

    print("\n--- FINAL RESEARCH SPEC ---")
    print(final_spec.model_dump_json(indent=2))
