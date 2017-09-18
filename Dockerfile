FROM jupyter/datascience-notebook:latest

RUN echo "Installing framework"
ADD . /tmp/
RUN cd /tmp/ && python /tmp/setup.py test
RUN cd /tmp/ && python /tmp/setup.py install

CMD ["start-notebook.sh", "--NotebookApp.token=''"]
