# GitAlert
- It will notice you **$ git push** of **develop** branch


## Python and Packages version
- Python 3.14.3
- requests 2.33.1
- winotify 1.1.0


## package install
```bash
python -m pip install requests winotify
```


## How To Use?
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
