sudo docker stop tiocps-left-monitoring
sudo docker rm tiocps-left-monitoring
sudo docker rmi rdpds/tiocps-left-monitoring
sudo docker pull rdpds/tiocps-left-monitoring:latest
sudo docker run -d --name tiocps-left-monitoring -p 5005:5005 rdpds/tiocps-left-monitoring

sudo docker stop tiocps-right-monitoring
sudo docker rm tiocps-right-monitoring
sudo docker rmi rdpds/tiocps-right-monitoring
sudo docker pull rdpds/tiocps-right-monitoring:latest
sudo docker run -d --name tiocps-right-monitoring -p 5006:5006 rdpds/tiocps-right-monitoring

sudo docker stop tiocps-h1-monitoring
sudo docker rm tiocps-h1-monitoring
sudo docker rmi rdpds/tiocps-h1-monitoring
sudo docker pull rdpds/tiocps-h1-monitoring:latest
sudo docker run -d --name tiocps-h1-monitoring -p 5007:5007 rdpds/tiocps-h1-monitoring

sudo docker stop tiocps-h2-monitoring
sudo docker rm tiocps-h2-monitoring
sudo docker rmi rdpds/tiocps-h2-monitoring
sudo docker pull rdpds/tiocps-h2-monitoring:latest
sudo docker run -d --name tiocps-h2-monitoring -p 5008:5008 rdpds/tiocps-h2-monitoring


sudo docker stop tiocps-h1-monitoring
sudo docker rm tiocps-h1-monitoring
sudo docker run -d --name tiocps-h1-monitoring -p 5007:5003 rdpds/tiocps-h1-monitoring

sudo docker stop tiocps-h2-monitoring
sudo docker rm tiocps-h2-monitoring
sudo docker run -d --name tiocps-h2-monitoring -p 5008:5004 rdpds/tiocps-h2-monitoring
