prepare:
    python -m src.prepare
train: prepare
    python -m src.train
demo-bad:
    python -m src.make_bad_batch
    python -m src.ingest data/incoming/bad_batch.parquet; test $$? -eq 1
demo-good:
    python -m src.ingest data/incoming/good_batch.parquet
	