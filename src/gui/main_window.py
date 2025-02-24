from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minecraft Server Manager")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #1e1e1e;")  # 黒基調

        # メインウィジェットの設定
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # レイアウト設定
        main_layout = QHBoxLayout(self.central_widget)

        # サイドバー作成
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # メインコンテンツ（画面切り替え）
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # サーバー作成画面
        self.server_setup_page = self.create_server_setup_page()
        self.stack.addWidget(self.server_setup_page)

        # メイン画面
        self.main_app_page = self.create_main_app_page()
        self.stack.addWidget(self.main_app_page)

        # 最初に表示する画面を選択
        self.stack.setCurrentWidget(self.server_setup_page)

    def create_sidebar(self):
        """サイドバーを作成（折りたたみ機能付き）"""
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()

        # 折りたたみボタン
        self.toggle_button = QPushButton("≡")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                font-size: 20px;
                border: none;
                padding: 10px;
                text-align: center;
                transition: transform 0.3s ease-in-out;
            }
            QPushButton:hover {
                background-color: #444444;
                transform: rotate(90deg);  /* 折りたたみボタンの回転効果 */
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # サイドバーの各ボタン
        self.server_button = self.create_sidebar_button("サーバー", "server_icon.png")
        self.manage_button = self.create_sidebar_button("管理", "manage_icon.png")
        self.settings_button = self.create_sidebar_button("設定", "settings_icon.png")
        self.help_button = self.create_sidebar_button("Help", "help_icon.png")

        # ボタンにクリックイベントを接続
        self.server_button.clicked.connect(self.show_server_page)
        self.manage_button.clicked.connect(self.show_manage_page)
        self.settings_button.clicked.connect(self.show_settings_page)
        self.help_button.clicked.connect(self.show_help_page)

        # ボタンをレイアウトに追加
        sidebar_layout.addWidget(self.toggle_button)
        sidebar_layout.addWidget(self.server_button)
        sidebar_layout.addWidget(self.manage_button)
        sidebar_layout.addWidget(self.settings_button)
        sidebar_layout.addWidget(self.help_button)

        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setStyleSheet("""
            background-color: #2d2d2d;
            border-right: 2px solid #444444;
            box-shadow: 4px 0 10px rgba(0, 0, 0, 0.3);
            border-radius: 10px 0 0 10px;  /* 丸みを帯びた角 */
        """)  # サイドバーの背景色と影
        sidebar_widget.setFixedWidth(180)  # 初期幅

        # サイズポリシーを設定して、折りたたみ可能にする
        sidebar_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        return sidebar_widget

    def toggle_sidebar(self):
        """サイドバーの表示/非表示を切り替える"""
        current_width = self.sidebar.width()
        if current_width == 180:  # サイドバーが表示されているとき
            self.animate_sidebar(50)  # サイドバーを折りたたむ
        else:
            self.animate_sidebar(180)  # サイドバーを元に戻す

    def animate_sidebar(self, width):
        """サイドバーのアニメーションを処理"""
        animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
        animation.setDuration(300)  # 300ミリ秒のスムーズなアニメーション
        animation.setStartValue(self.sidebar.width())
        animation.setEndValue(width)
        animation.start()

        # サイズ変更後の更新処理
        animation.finished.connect(self.update_sidebar_size)

    def update_sidebar_size(self):
        """サイズ変更後にレイアウトの更新を行う"""
        self.sidebar.updateGeometry()

    def create_sidebar_button(self, text, icon_path):
        """サイドバー用のカスタムボタン作成"""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))  # アイコンをボタンに設定
        button.setIconSize(QSize(24, 24))  # アイコンサイズを調整
        button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                font-size: 16px;
                border: none;
                padding: 10px;
                text-align: left;
                width: 160px;
                border-radius: 5px;
                transition: background-color 0.3s ease, padding 0.3s ease;
            }
            QPushButton:hover {
                background-color: #444444;
                padding-left: 20px;  /* ホバー時に少し右に動く */
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        return button

    def create_server_setup_page(self):
        """サーバー作成画面"""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("サーバーが見つかりません。\n新規作成してください。")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        create_button = self.create_custom_button("新しいサーバーを作成")
        create_button.clicked.connect(self.create_server)
        layout.addWidget(create_button)

        page.setLayout(layout)
        return page

    def create_main_app_page(self):
        """メインアプリのページ"""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Minecraft サーバーマネージャー")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(label)

        self.server_management_page = self.create_server_management_page()
        layout.addWidget(self.server_management_page)

        page.setLayout(layout)
        return page

    def create_server_management_page(self):
        """サーバー管理ページ"""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("サーバー管理画面")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        start_button = self.create_custom_button("サーバーを起動")
        stop_button = self.create_custom_button("サーバーを停止")
        layout.addWidget(start_button)
        layout.addWidget(stop_button)

        page.setLayout(layout)
        return page

    def create_settings_page(self):
        """設定画面"""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("設定画面")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        page.setLayout(layout)
        return page

    def create_help_page(self):
        """Help画面"""
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("ヘルプページ")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        page.setLayout(layout)
        return page

    def show_server_page(self):
        """サーバー画面を表示"""
        self.stack.setCurrentWidget(self.server_setup_page)

    def show_manage_page(self):
        """管理画面を表示"""
        self.stack.setCurrentWidget(self.main_app_page)

    def show_settings_page(self):
        """設定画面を表示"""
        self.stack.setCurrentWidget(self.create_settings_page())

    def show_help_page(self):
        """Help画面を表示"""
        self.stack.setCurrentWidget(self.create_help_page())

    def create_custom_button(self, text):
        """カスタムボタン作成"""
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #397539;
            }
        """)
        return button


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
