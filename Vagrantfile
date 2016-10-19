# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
require 'rbconfig'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"
    config.vm.synced_folder ".", "/vagrant"
    config.vm.provider "virtualbox" do |vb|
        vb.name = "challenge-server-web"
    end

    config.vm.network "forwarded_port", guest: 5000, host: 8000
    config.vm.network "public_network"

    config.vm.define "localhost"
    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "devops/setup.yml"
        ansible.verbose = "vvv"
        ansible.groups = {
            "web" => ["localhost"],
            "redis" => [],
        }
    end
end
