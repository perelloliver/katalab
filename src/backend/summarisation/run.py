from dotenv import load_dotenv
from ..utils import get_logger, read_documents_from_directory
from .role import summarise_role_information

logger = get_logger(__name__)

def run():
    load_dotenv()
    logger.info("Starting summarisation run")
    docs = read_documents_from_directory("case-studies/nebula_junior_dev/company")
    result = summarise_role_information(docs)
    print(result.model_dump_json(indent=2))
    logger.info("Run completed successfully")

if __name__ == "__main__":
    run()
# uv command for this: 