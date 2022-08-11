FROM python:3.8
LABEL maintainer="joshua.santiago14@upr.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app/main.py"]