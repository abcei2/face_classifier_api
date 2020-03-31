# Docker of face_classifier flask api

## install docker

sudo apt-get update

sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -


### Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88, by searching for the last 8 characters of the fingerprint.

sudo apt-key fingerprint 0EBFCD88
### Show something like this

```ruby
pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]
```
### for OS x86_64/amd64 architecture

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

### then
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

### test
sudo docker run hello-world

## Excecute

### Go to main folder
cd face_reco_api/

### build container
sudo docker build -t face_recognizer:latest .

### run container in port 5000
sudo docker run -p 5000:5000 face_recognizer:latest

# Functions

This api allows to:

### Register faces (upload image of face)
### Detect faces on an images
### Update_face_model

# REFS
## https://docs.docker.com/install/linux/docker-ce/ubuntu/