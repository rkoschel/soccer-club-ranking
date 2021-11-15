
# setup and start bot clock service
sudo cp ~pi/soccer-club-ranking/setup/scr.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/scr.service
sudo systemctl daemon-reload
sudo systemctl enable scr.service
sudo systemctl start scr.service