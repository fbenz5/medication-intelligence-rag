FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml .
COPY src ./src
COPY data/processed/chunks.jsonl ./data/processed/chunks.jsonl
COPY data/raw/CIS_bdpm.txt ./data/raw/CIS_bdpm.txt
COPY data/raw/CIS_CIP_bdpm.txt ./data/raw/CIS_CIP_bdpm.txt
COPY data/raw/CIS_COMPO_bdpm.txt ./data/raw/CIS_COMPO_bdpm.txt

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "medintel.api:app", "--host", "0.0.0.0", "--port", "8000"]