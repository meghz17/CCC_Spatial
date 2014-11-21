#!/bin/sh

sudo apt-get update
sudo apt-get install -y vim git

sudo apt-get install -y python-pip 
sudo apt-get install -y cython python-numpy python-scipy python-matplotlib

pip install ipython[all]
pip install geopy guess_language_spirit requests pymongo

pip install git+https://github.com/Permafacture/pygmaps-ng.git#Egg=pygmaps_ng
