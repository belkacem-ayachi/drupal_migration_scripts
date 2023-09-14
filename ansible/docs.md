# Installing Ansible 
- python3 -m pip install ansible
- Allow root to connect via ssh
- change the password of root to 'UNescwa2023@@'
- generate rsa key ssh-keygen -t rsa
- ssh-copy-id -p 22 i- <PATH_TO_KEY> root@10.30.42.24

# Installing ansible on the client
run:

    sudo apt update -y 
    sudo apt install -y software-properties-common
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt install -y ansible

# Test connection
cat hosts
ansible -i hosts all -m ping
