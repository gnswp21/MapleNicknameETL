#!/bin/bash
cd ~
# 스크립트 실행 시 에러 발생 시 중단
set -e
# 시스템 업데이트 및 JDK 설치를 위한 패키지 인덱스 업데이트
sudo apt update
# OpenJDK 11 설치
sudo apt install -y openjdk-11-jdk
# JAVA_HOME 환경 변수 설정
echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc
