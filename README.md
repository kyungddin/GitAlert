# GitAlert
- It will notice you **$ git push** of **develop** branch


## Install & Execution
- 1. Use Git Clone to download files
    ```bash
    git clone https://github.com/kyungddin/GitAlert.git
    ```
- 2. Execute GitAlert.exe
- 3. Enter your Bitbucket Info and Start!


## Structure
- main.py
    - alert.py
    - config.py
    - gui.py


## Python and Packages version
- Python 3.14.3
    - requests 2.33.1
    - winotify 1.1.0
    - PySide6 6.11.0
    - pyinstaller-6.20.0


## package install
```bash
python -m pip install requests winotify PySide6 pyinstaller
```

## For Developer
1. Create Bitbucket Token
    - Profile - Manage account - Personal access tokens
    - Create a token (All Settings are **default**)
    - Copy Your Token (Only one chance to copy)

2. Paste Your Token to **main.py**
    ```python
    ACCESS_TOKEN = "paste_your_token_here"
    ```

3. run main.py
    ```bash
    python main.py
    ```
4. build python sources
    ```bash
    pyinstaller --onefile --noconsole --icon="git_alert.ico" --distpath . --name "GitAlert" main.py --clean
    ```

    ```bash
    pyinstaller --onefile --noconsole --distpath . --name "GitAlert" main.py --clean
    ```

