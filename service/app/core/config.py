from pathlib import Path

from dynaconf import Dynaconf, LazySettings

BASE_DIR: Path = Path(__file__).resolve().parent.parent

settings: LazySettings = Dynaconf(
    settings_files=[BASE_DIR / "core/config.yml", BASE_DIR / "core/.secrets.yml"],
    environments=True,
    dotenv_path=BASE_DIR / ".env",
    envvar_prefix=False,
)
