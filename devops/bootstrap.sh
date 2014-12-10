#!/usr/bin/env bash
vagrant_dir='/vagrant'
devops_dir="${vagrant_dir}/devops"
req_dir="${devops_dir}/requirements"
vagrant_home='/home/vagrant'

# Add keys

# Update the vm
apt-get update
apt-get upgrade -y

# Install system packages
cat ${req_dir}/ubuntu.txt | xargs apt-get install -y

# Install libraries
pip install -r ${req_dir}/python.txt

# Provide quick access for vagrant directory
ln -s $vagrant_dir ${vagrant_home}/v

# Install dotfiles
su vagrant -c "source ${devops_dir}/dotfiles.sh"
