FROM python:3.8
LABEL maintainer="lorenz.vanthillo@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5050
ENTRYPOINT ["python"]
CMD ["app/main.py"]