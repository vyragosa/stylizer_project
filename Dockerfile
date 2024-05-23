FROM continuumio/miniconda3

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "stylizer_env", "/bin/bash", "-c"]

RUN pip install -r requirements.txt

CMD ["conda", "run", "-n", "stylizer_env", "python", "manage.py", "runserver", "0.0.0.0:8000"]
