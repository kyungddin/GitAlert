import time
import requests
from winotify import Notification

# =============================== Configuration ===============================
BITBUCKET_URL = "url"
PROJECT_KEY = "project"       # 프로젝트 키
REPO_SLUG = "repo"           # 레포 슬러그
# ****************************** Paste Token Here ******************************

ACCESS_TOKEN = "token"     

# ******************************************************************************
BRANCH = "dranch"                      # 감시할 브랜치
POLLING_INTERVAL = 60                  # 폴링 주기 (초)
# ==============================================================================

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_latest_commit():
    url = f"{BITBUCKET_URL}/rest/api/1.0/projects/{PROJECT_KEY}/repos/{REPO_SLUG}/commits"
    params = {"until": BRANCH, "limit": 1}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, verify=False)
        response.raise_for_status()
        data = response.json()
        return data['values'][0] if data['values'] else None
    except Exception as e:
        print(f"API 요청 실패: {e}")
        return None

def send_notification(commit):
    author = commit['author']['name']
    message = commit['message'].split('\n')[0]  # 커밋 메시지 첫 줄만
    
    toast = Notification(
        app_id="GitAlert",
        title=f"📌 [{REPO_SLUG}] Push 알림",
        msg=f"{author}: {message}",
        duration="short"
    )
    toast.show()
    print(f"알림 전송: {author} - {message}")

def main():
    print(f"감시 시작: {REPO_SLUG} / {BRANCH} (주기: {POLLING_INTERVAL}초)")
    
    # 시작 시 현재 최신 커밋을 기준점으로 저장
    last_commit = get_latest_commit()
    if last_commit:
        print(f"기준 커밋: {last_commit['id'][:7]} - {last_commit['message'].split(chr(10))[0]}")
    
    while True:
        time.sleep(POLLING_INTERVAL)
        
        latest_commit = get_latest_commit()
        
        if latest_commit and last_commit:
            if latest_commit['id'] != last_commit['id']:
                send_notification(latest_commit)
                last_commit = latest_commit

if __name__ == '__main__':
    main()
