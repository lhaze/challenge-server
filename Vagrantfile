# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"
    config.vm.synced_folder ".", "/vagrant"
    config.vm.provision "shell", :path => "devops/install_ansible.sh"
    #config.vm.provision "shell", :path => "devops/play_web.sh"

    #config.vm.provision :shell, :path => "build_redis.sh"
    #config.vm.provision :shell, :path => "install_redis.sh"
    #config.vm.provision :shell, :path => "install_sentinel.sh"
    #config.vm.provision :file, :source => ".bash_profile", :destination => "/home/vagrant/.bash_profile"

    config.vm.provider "virtualbox" do |vb|
        vb.name = "snakes-web"
    end
    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # config.vm.network "forwarded_port", guest: 8000, host: 8000
    # config.vm.provider "virtualbox" do |vb|
        # Don't boot with headless mode
        # vb.gui = true
    # end
    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    # config.vm.network "private_network", ip: "192.168.33.10"

    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"
end
