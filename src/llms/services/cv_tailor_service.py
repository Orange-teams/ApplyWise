from src.utils.prompt_loader import load_prompts


class CVTailorService:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider
        self.prompts = load_prompts()

    def tailor_resume(
        self,
        master_tex: str,
        job_description: str,
    ) -> str:
        prompt_cfg = self.prompts["cv_revise"]
        system_prompt = prompt_cfg["system"]

        user_prompt = prompt_cfg["user"].format(
            master_tex=master_tex,
            job_description=job_description,
        )

        return self.llm_provider.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )