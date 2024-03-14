### auth_rclone.py
Paperspace Gradient doesn't charge you for the files stored in the /tmp directory so it's useful to use GoogleDrive as a permanent storage and /tmp as a temporary one.
This script will automate the tedious authetication required in rclone necessary for uploading & downloading files from Google Drive.
I am not an expert in security and this script is probably vulnerable.
Please use at your own risk.

### Usage
Manually authenticate first using `rclone config`.  
Then copy the config file to the /notebooks directory
```python
cp ~/.config/rclone/rclone.conf /notebooks/rclone.conf
```

- Refresh current token
Use this command whenever you create a new gradient instance
```python
python refresh.py /notebooks/rclone.conf ~/.config/rclone/rclone.conf
```

- Initialize refresh token
Use this whenever the refresh token is expired
```python
python init.py /notebooks/rclone.conf ~/.config/rclone/rclone.conf
```
