from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow  # 作成したMainWindowクラスのインポート

if __name__ == "__main__":
    app = QApplication([])  # アプリケーションのインスタンス作成
    window = MainWindow()    # MainWindowのインスタンス作成
    window.show()            # ウィンドウ表示
    app.exec_()              # イベントループを開始
