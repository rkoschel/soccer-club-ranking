
sudo pip install flask
sudo pip install beautifulsoup4

# setup and start bot clock service
sudo cp ~pi/soccer-club-ranking/pi-setup/scr.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/scr.service
sudo systemctl daemon-reload
sudo systemctl enable scr.service
sudo systemctl start scr.service