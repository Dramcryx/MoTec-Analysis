FROM python:3.9.9-bullseye
RUN apt-get update
RUN apt-get install -y openjdk-11-jre
RUN pip install clickhouse-driver pyspark docker
COPY ./util /spark/util/
COPY ./clickhouse-loader /spark/
COPY ./preprocessor /spark/
COPY ./spark.py /spark/
COPY ./execpipeline.sh /spark/
WORKDIR ./spark
RUN ln -fs /usr/local/bin/python /usr/bin/python