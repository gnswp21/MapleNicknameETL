#!/bin/bash
cd /home/ubuntu
curl https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz --output kafka.tgz
tar -xvf kafka.tgz
ln -s kafka_2.12-2.5.0 kafka
