FROM python:3.7

RUN mkdir -p /opt/easyops
RUN mkdir -p /var/log/easyops
RUN mkdir -p /var/run

COPY ./easyops /opt/easyops/easyops
COPY ./config.py /opt/easyops
COPY ./gunicorn.conf.py /opt/easyops
COPY ./inventory.py /opt/easyops
COPY ./requirements.txt /opt/easyops
COPY ./manage.py /opt/easyops
COPY ./README.md /opt/easyops

WORKDIR /opt/easyops

RUN pip install -r /opt/easyops/requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com --trusted-host pypi.douban.com

CMD ["gunicorn", "manage:easyops", "-c", "/opt/easyops/gunicorn.conf.py"]