FROM conda/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f /app/environment.yml

SHELL ["conda", "run", "-n", "stylizer_env", "/bin/bash", "-c"]

COPY . /app

RUN pip install -r requirements.txt

CMD ["conda", "run", "-n", "stylizer_env", "python", "manage.py", "runserver", "0.0.0.0:8000"]
