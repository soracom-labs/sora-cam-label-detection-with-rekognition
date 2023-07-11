#!/bin/bash
echo "Begin install..."

sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel
wget https://www.python.org/ftp/python/3.9.17/Python-3.9.17.tgz
tar xvf Python-3.9.17.tgz
cd Python-3.9.17
./configure --enable-optimizations --prefix=$HOME/.local
sudo make altinstall
cd ..
sudo rm -rf Python-3.9.17 Python-3.9.17.tgz
python3.9 --version
pip3.9 --version

echo "Install completed!!"