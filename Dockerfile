FROM python:3.12

WORKDIR /app
COPY . /app
RUN pip install -r req.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --upgrade urllib3 requests
RUN pip install pymssql -U
RUN pip install itsdangerous
RUN pip install pip_libs/golem_framework-0.9.1-py3-none-any.whl

EXPOSE 8000
WORKDIR /app/Kofile
CMD ["python","run_waitress.py"]