
# FTP Backup Script

The FTP Backup Script is a Python script designed to automatically backup files from an FTP server to a local directory. It uses the `ftplib` library to connect to the FTP server and transfer files.

## Requirements

- Python 3 - To install Python 3, please visit the official website: [https://www.python.org/](https://www.python.org/)
- ftplib - To install the required library, use the following command:
  ```bash
  pip install pyftpdlib
  ```

## Configuration

Run the script a first time to create `ini.json` with default parameters then configure the `ini.json` file in the same directory as the script. The `ini.json` file contains the following parameters:

- `"server"`: The FTP server address.
- `"username"`: The FTP server username.
- `"password"`: The FTP server password.
- `"remote_path"`: The remote path on the FTP server from where files will be backed up.
- `"local_path"`: The local directory where the backup files will be saved.
- `"backup_Hour"`: The time at which the backup will be executed in the format "HH:MM" (e.g., "02:30" for 2:30 AM).
- `"days_before_removing_backup"`: The number of days after which backup files will be removed from the local directory to manage disk space.

## Usage

1. Configure the `ini.json` file with your FTP server and backup parameters.

2. Run the FTP Backup Script using Python 3:
   ```bash
   python3 GetBackups.py
   ```

The script will connect to the FTP server, check for new files in the specified remote path, and download them to the local directory. It will also remove files older than the specified number of days (default is 7 days) from the local directory to manage disk space.

## Note

- The script assumes that the backup files on the FTP server have filenames starting with "Backup_" and followed by the date in the format "YYYY-MM-DD" (e.g., Backup_2023-07-19.zip).
- The `days_before_removing_backup` variable specifies the number of days after which backup files will be removed from the local directory to maintain disk space.

## Author

- [Noy](https://github.com/4Noy)

## Version

- 0.1
