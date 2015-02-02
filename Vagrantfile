VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"
    config.ssh.forward_agent = true

    config.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 4
      v.name = "ubuntu-devbox"
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      #v.gui = true # if hangs, uncomment to see whats going on
    end

    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.network "forwarded_port", guest: 8000, host: 9000
    config.vm.network "forwarded_port", guest: 8001, host: 9001
    config.vm.network "forwarded_port", guest: 8002, host: 9002
    config.vm.network :private_network, ip: '192.168.222.220' #ensure does not conflict

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook.yml"
      ansible.host_key_checking = false
      ansible.extra_vars = { ansible_ssh_user: 'vagrant', 
              ansible_connection: 'ssh',
              ansible_ssh_args: '-o ForwardAgent=yes'}
    end

    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.synced_folder "~/projects", "/home/vagrant/projects", nfs: true #nfs requires private network
    config.vm.synced_folder "~/.ssh", "/host_ssh", create: true #, nfs: true
  #end
end
