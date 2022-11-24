# Fshare Tool - Download, save and upload to Google Drive, OneDrive using Fshare API.

## Introduction

Fshare Tool is a tool to transfer Fshare file to Google Drive, OneDrive using Fshare API.

## Requirements
- You need to have a VIP Fshare with daily bandwith available account to use this tool (to can download file with high speed).
- A VPS with high speed internet connection (to can upload file to Google Drive, OneDrive with high speed), and can have unlimited bandwith.

## Before install
- Create API app for Fshare: go to [this page](https://www.fshare.vn/api-doc). Click `Get App Key` button, then fill the form and click `Submit` button. You will get `App Key` and `App Secret` for your app via email.

## Installation 
- Bellow instruction is for Ubuntu 20.04 and any Debian distro, but you can install on other Linux distro with some changes.
- Update and install Python 3 (`>= 3.6`)

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip git
    ```

- If you want to upload to Google Drive, install `gdrive`, you can follow home page of [gdrive](https://github.com/prasmussen/gdrive) to install. Make sure you can run `gdrive` command in terminal.

- If you want to upload to OneDrive, install `rclone`, you can follow home page of [rclone](https://rclone.org/) to install. Make sure you can run `rclone` command in terminal. After install, you need to config `rclone` to use OneDrive, you can follow [this guide](https://rclone.org/onedrive/).

- Clone this repo and install dependencies

    ```bash
    git clone https://github.com/lvdat/fshare_tool
    cd fshare_tool
    pip3 install -r requirements.txt
    ```

- Make a copy of `config.ini.example` to `config.ini` and edit it.

    ```bash
    cp config.ini.example config.ini
    vim config.ini
    ```
> You must config `mail`, `password` of your Fshare Account, and `app_agent`, `app_key` your received from Fshare via mail.
> Morever, you want config `Drive` block to can use upload function: If use Google Drive, set `gdrive` to `1` and config `folder_id`. If use OneDrive, set `onedrive` to `1`, config `rclone_remote_name` and `onedrive_folder_path`.

## Usage
All done, before use upload, you must login to Fshare API by run this command:

```bash
python3 login_fshare.py
```
If output is `Done!`, you are logged in successfully.

To upload file from Fshare link to Drive, use:
```bash
python3 f_dl.py <url of Fshare file> [Password of link (opitional)]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change