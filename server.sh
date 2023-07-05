sudo docker stop tiocps-left-monitoring
sudo docker rm tiocps-left-monitoring
sudo docker rmi rdpds/tiocps-left-monitoring

sudo docker stop tiocps-right-monitoring
sudo docker rm tiocps-right-monitoring
sudo docker rmi rdpds/tiocps-right-monitoring

sudo docker stop tiocps-h1-monitoring
sudo docker rm tiocps-h1-monitoring
sudo docker rmi rdpds/tiocps-h1-monitoring

sudo docker stop tiocps-h2-monitoring
sudo docker rm tiocps-h2-monitoring
sudo docker rmi rdpds/tiocps-h2-monitoring
