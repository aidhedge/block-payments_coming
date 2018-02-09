FROM python:3
EXPOSE 7006
ENV FLASK_DEBUG=1
ENV PORT=7006
RUN pip install flask
RUN pip install cerberus
RUN pip install requests
