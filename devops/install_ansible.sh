#!/usr/bin/env bash
sudo apt-get install -y software-properties-common python-dev python-pip
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible
