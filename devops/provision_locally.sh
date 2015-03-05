#!/bin/bash
#
# Windows shell provisioner for Ansible playbooks, based on Jeff Geerling's
# windows-vagrant-ansible: https://github.com/geerlingguy/JJG-Ansible-Windows
#
# @see README.md
# @author Jeff Geerling, 2014

# Uncomment if behind a proxy server.
# export {http,https,ftp}_proxy='http://username:password@proxy-host:80'

ANSIBLE_PLAYBOOK=$1
DIR="/vagrant"
REQUIREMENTS_DIR="${DEVOPS_DIR}/devops/requirements"

# Make sure Ansible playbook exists.
if [ ! -f $DIR/$ANSIBLE_PLAYBOOK ]; then
  echo "Cannot find Ansible playbook: ${DEVOPS_DIR}/${ANSIBLE_PLAYBOOK}"
  exit 1
fi

# Install Ansible roles from requirements file, if available.
if [ -f $REQUIREMENTS_DIR/requirements/ansible.txt ]; then
  sudo ansible-galaxy install -r $REQUIREMENTS_DIR/requirements/ansible.txt
fi

# Run the playbook.
echo "Running Ansible provisioner defined in Vagrantfile."
ansible-playbook -i 'web,' -c local ${DIR}/${ANSIBLE_PLAYBOOK} --extra-vars "is_windows=true"
