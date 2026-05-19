from src.core.exceptions import JobNotFoundException
from src.db.session import SessionLocal
from src.services.job_service import JobService
from src.llms.gemini_provider import GeminiProvider
from src.llms.services.cv_tailor_service import CVTailorService
from src.resume.storage.resume_storage import ResumeStorage
from src.resume.compiler.latex_compiler import LatexCompiler
from config.settings import settings
from pathlib import Path
class CVTailoringPipeline:

    def run(self, job_id: int):

        db = SessionLocal()

        job_service = JobService(db)
        try:
            job = job_service.get_job(job_id)
        except JobNotFoundException as e:
            print(e)
            return


        storage = ResumeStorage()

        master_tex = storage.load_template(
            settings.MASTER_RESUME_PATH
        )
        provider = GeminiProvider()

        tailor_service = CVTailorService(provider)

        tailored_tex = tailor_service.tailor_resume(
            master_tex=master_tex,
            job_description=job.job_description,
        )

        tex_filename = f"{job.id}.tex"
        tex_path = str(Path(settings.GENERATED_TEX_PATH) / tex_filename)
        print(tex_path)
        storage.save_tex(tex_path, tailored_tex)
        compiler = LatexCompiler()

        compiler.compile(
            tex_path=tex_path,
            output_dir=settings.GENERATED_TEX_PATH,
        )