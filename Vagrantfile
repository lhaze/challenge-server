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

    is_windows = (RbConfig::CONFIG['host_os'] =~ /mswin|mingw|cygwin/)
    if is_windows
        # provisioning with shell script (and local Ansible within VM)
        config.vm.provision "shell", :path => "devops/install_ansible.sh"
        config.vm.provision "shell" do |sh|
            sh.path = "devops/provision_locally.sh"
            sh.args = "devops/setup_playbook.yml"
        end
    else
        # provisioning with Ansible through SSH.
        config.vm.provision "ansible" do |ansible|
            ansible.playbook = "devops/setup_playbook.yml"
            ansible.inventory_path = "web,"
            ansible.sudo = true
        end
    end
end
