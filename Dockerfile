FROM python:3.12.2-slim-bullseye
WORKDIR /app
EXPOSE 55582
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "app.py" ]
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]