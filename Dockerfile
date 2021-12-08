FROM python:3.9.9-bullseye
RUN apt-get update
RUN apt-get install -y openjdk-11-jre
RUN pip install clickhouse-driver
RUN wget https://files.pythonhosted.org/packages/d4/0e/4528c9703863fc4df49fd4425c6f15ee5f370cff9e43cea3f8076b034e3f/pyspark-3.2.0.tar.gz
RUN pip install ./pyspark-3.2.0.tar.gz
COPY ./util /spark/util/
COPY ./clickhouse-loader /spark/
COPY ./preprocessor /spark/
COPY ./spark.py /spark/
COPY ./execpipeline.sh /spark/
WORKDIR ./spark
RUN ln -fs /usr/local/bin/python /usr/bin/python