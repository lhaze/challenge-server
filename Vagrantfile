# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"
    config.vm.synced_folder ".", "/vagrant"
    config.vm.provider "virtualbox" do |vb|
        vb.name = "challenge-server-web"
    end

    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.network "private_network", ip: "192.168.33.10"
    config.vm.network "public_network"

    # Pass the configuration flow to the Ansible installed inside the VM
    config.vm.provision "shell", :path => "devops/install_ansible.sh"
    config.vm.provision "shell" do |s|
        s.inline = "ansible-playbook"
        s.args = ["devops/setup.yml", "-i", "devops/inventory_windows.sh"]
    end
end
