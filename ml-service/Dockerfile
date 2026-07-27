# build context is the repo root (needs data-generator/), e.g.:
#   docker build -f ml-service/Dockerfile -t ad-vault/ml-service .
FROM python:3.12-slim

WORKDIR /app
COPY ml-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# generate synthetic data and train the model at build time, so the image
# ships with a ready-to-serve model.joblib instead of depending on a volume
WORKDIR /data-generator
COPY data-generator/generate_data.py .
RUN python generate_data.py --output-dir /data-generator/output

WORKDIR /app
COPY ml-service/ .
RUN python train.py

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
