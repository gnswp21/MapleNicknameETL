#!/bin/bash
exec /home/ubuntu/MapleNicknameETL/kafka/jdk11-install.sh
cd /home/ubuntu
curl https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz --output kafka.tgz
tar -xvf kafka.tgz
ln -s kafka_2.12-2.5.0 kafka
apt-get update && apt-get install -y gettext
exec /home/ubuntu/MapleNicknameETL/kafka/kafka-init.sh

mkdir -p /var/lib/zookeeper
