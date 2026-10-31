import logging, shutil, sys, pathlib, pandas as pd, pandera.pandas as pa
from src.contract import schema

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ingest")

def ingest(path):
    path = pathlib.Path(path)
    df = pd.read_parquet(path)
    try:
        schema.validate(df, lazy=True)       # lazy junta todas as falhas
    except pa.errors.SchemaErrors as e:
        qdir = pathlib.Path("data/quarantine"); qdir.mkdir(exist_ok=True)
        shutil.move(path, qdir / path.name)
        e.failure_cases.to_csv(qdir / f"{path.stem}_errors.csv", index=False)
        log.error("batch=%s BLOQUEADO: %d falhas, movido para quarentena", path.name, len(e.failure_cases))
        return False
    log.info("batch=%s OK: %d linhas", path.name, len(df))
    return True

if __name__ == "__main__":
    sys.exit(0 if ingest(sys.argv[1]) else 1)
    