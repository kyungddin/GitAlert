import sys
from PySide6.QtWidgets import QApplication, QDialog

from config import load_config
from gui import SetupDialog, MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 저장된 설정 불러오기
    cfg = load_config()

    # 시작 시 항상 설정 다이얼로그 표시
    dlg = SetupDialog(cfg)
    dlg.move(
        app.primaryScreen().geometry().center().x() - dlg.sizeHint().width() // 2,
        app.primaryScreen().geometry().center().y() - 180,
    )
    if dlg.exec() != QDialog.Accepted:
        sys.exit(0)   # 취소하면 앱 종료

    cfg = dlg.get_config()

    # 메인 윈도우 실행
    window = MainWindow(cfg)
    window.resize(780, 540)
    window.move(
        app.primaryScreen().geometry().center().x() - 390,
        app.primaryScreen().geometry().center().y() - 270,
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
