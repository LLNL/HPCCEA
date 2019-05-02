FROM python:2.7
RUN pip install prometheus_client
RUN apt-get update && apt-get install -y ipmitool
COPY ipmi_exporter.py /

# Set environment variables
ENV TARGET_IPS ""

EXPOSE 8000
CMD ["python", "ipmi_exporter.py"]