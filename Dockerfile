FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./model ./model
COPY ./app ./app
COPY .streamlit .streamlit
COPY frontend.py .
COPY run.sh .
RUN chmod +x run.sh
EXPOSE 10000
CMD ["bash", "run.sh"]
