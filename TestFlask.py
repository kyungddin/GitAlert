from flask import Flask, request
from winotify import Notification

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if 'commits' not in data:
        return 'OK', 200
    
    pusher = data['pusher']['name']
    repo = data['repository']['name']
    branch = data['ref'].split('/')[-1]
    commits = len(data['commits'])
    
    message = f"{pusher}님이 {branch} 브랜치에 {commits}개 커밋 푸시"
    
    try:
        toast = Notification(
            app_id="GitAlert",
            title=f"📌 [{repo}] Push 알림",
            msg=message,
            duration="short"
        )
        toast.show()
        print("토스트 알림 성공")
    except Exception as e:
        print(f"토스트 알림 실패: {e}")
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
