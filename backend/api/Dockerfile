FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --user -r requirements.txt

COPY . .

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

ENV PATH=/root/.local/bin:$PATH

ENV PORT=8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--timeout=600", "run:app", "--log-file", "-"]