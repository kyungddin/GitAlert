import time
import requests
from PySide6.QtCore import QThread, Signal


class MonitorThread(QThread):
    log   = Signal(str)        # 로그 메시지 → GUI
    alert = Signal(str, str)   # (제목, 내용) → 윈도우 알림

    def __init__(self, cfg: dict):
        super().__init__()
        self._running = True
        self._cfg = cfg
        self._headers = {
            "Authorization": f"Bearer {cfg['token']}",
            "Content-Type": "application/json",
        }

    def stop(self):
        self._running = False

    def run(self):
        cfg = self._cfg
        branches = cfg["branches"]
        interval = cfg["polling_interval"]
        repo     = cfg["repo"]

        self.log.emit(f"감시 시작: {repo} / {branches} (주기: {interval}s)")

        # 브랜치별 기준 커밋 초기화
        last_commits = {}
        for branch in branches:
            commit = self._get_latest_commit(branch)
            last_commits[branch] = commit
            if commit:
                short_id = commit["id"][:7]
                msg = commit["message"].split("\n")[0]
                self.log.emit(f"[{branch}] 기준 커밋: {short_id} - {msg}")

        # 폴링 루프
        while self._running:
            # 1초씩 쪼개서 자야 stop() 호출 시 즉시 반응
            for _ in range(interval):
                if not self._running:
                    return
                time.sleep(1)

            for branch in branches:
                latest = self._get_latest_commit(branch)
                last   = last_commits.get(branch)
                if latest and last and latest["id"] != last["id"]:
                    author = latest["author"]["name"]
                    msg    = latest["message"].split("\n")[0]
                    self.log.emit(f"[{branch}] 새 커밋 감지: {author} - {msg}")
                    self.alert.emit(
                        f"📌 [{repo}/{branch}] Push 알림",
                        f"{author}: {msg}",
                    )
                    last_commits[branch] = latest

    def _get_latest_commit(self, branch: str):
        cfg = self._cfg
        url = (
            f"{cfg['url']}/rest/api/1.0/projects/{cfg['project']}"
            f"/repos/{cfg['repo']}/commits"
        )
        try:
            resp = requests.get(
                url,
                headers=self._headers,
                params={"until": branch, "limit": 1},
                verify=False,
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["values"][0] if data["values"] else None
        except Exception as e:
            self.log.emit(f"[{branch}] API 요청 실패: {e}")
            return None
