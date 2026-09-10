from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QApplication,
)
from PyQt5.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QLinearGradient,
)


class SplashScreen(QDialog):

    def __init__(self):
        super().__init__()

        self.setFixedSize(650, 400)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # -----------------------------
        # Layout
        # -----------------------------

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            60, 50, 60, 40
        )

        # -----------------------------
        # Welcome
        # -----------------------------

        welcome = QLabel("WELCOME TO")

        welcome.setAlignment(Qt.AlignCenter)

        welcome.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 11px;
                font-weight: bold;
                background: transparent;
            }
        """)

        layout.addWidget(welcome)

        # -----------------------------
        # MAZE
        # -----------------------------

        maze = QLabel("MAZE")

        maze.setAlignment(Qt.AlignCenter)

        maze.setStyleSheet("""
            QLabel {
                color: #62E38A;
                font-size: 64px;
                font-weight: 900;
                background: transparent;
            }
        """)

        layout.addWidget(maze)

        # -----------------------------
        # PAINT
        # -----------------------------

        paint = QLabel("PAINT")

        paint.setAlignment(Qt.AlignCenter)

        paint.setStyleSheet("""
            QLabel {
                color: #F2F4F8;
                font-size: 28px;
                font-weight: 900;
                background: transparent;
            }
        """)

        layout.addWidget(paint)

        # -----------------------------
        # Subtitle
        # -----------------------------

        subtitle = QLabel(
            "Paint every corridor."
        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 13px;
                background: transparent;
            }
        """)

        layout.addWidget(subtitle)

        layout.addStretch()

        # -----------------------------
        # Status
        # -----------------------------

        self.status = QLabel(
            "INITIALIZING..."
        )

        self.status.setAlignment(Qt.AlignCenter)

        self.status.setStyleSheet("""
            QLabel {
                color: #8F96A5;
                font-size: 10px;
                font-weight: bold;
                background: transparent;
            }
        """)

        layout.addWidget(self.status)

        # -----------------------------
        # Progress
        # -----------------------------

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)

        self.progress.setValue(0)

        self.progress.setTextVisible(False)

        self.progress.setFixedHeight(7)

        self.progress.setStyleSheet("""
            QProgressBar {
                background: #1A1E27;
                border: none;
                border-radius: 4px;
            }

            QProgressBar::chunk {
                background: #62E38A;
                border-radius: 4px;
            }
        """)

        layout.addWidget(self.progress)

        # -----------------------------
        # Version
        # -----------------------------

        version = QLabel(
            "MazePaint • v1.0"
        )

        version.setAlignment(Qt.AlignCenter)

        version.setStyleSheet("""
            QLabel {
                color: #4F5665;
                font-size: 10px;
                background: transparent;
            }
        """)

        layout.addWidget(version)

        # -----------------------------
        # Animation
        # -----------------------------

        self.value = 0

        # Fade in

        self.setWindowOpacity(0)

        self.fade = QPropertyAnimation(
            self,
            b"windowOpacity"
        )

        self.fade.setDuration(500)

        self.fade.setStartValue(0)

        self.fade.setEndValue(1)

        self.fade.setEasingCurve(
            QEasingCurve.OutCubic
        )

    # =====================================
    # PAINT
    # =====================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        rect = self.rect().adjusted(
            2, 2, -2, -2
        )

        gradient = QLinearGradient(
            rect.topLeft(),
            rect.bottomRight()
        )

        gradient.setColorAt(
            0,
            QColor("#171A22")
        )

        gradient.setColorAt(
            1,
            QColor("#0D1015")
        )

        painter.setBrush(gradient)

        painter.setPen(
            QColor("#2A303B")
        )

        painter.drawRoundedRect(
            rect,
            24,
            24
        )

        # Green border

        painter.setBrush(Qt.NoBrush)

        painter.setPen(
            QColor(98, 227, 138, 60)
        )

        painter.drawRoundedRect(
            rect,
            24,
            24
        )

    # =====================================
    # START
    # =====================================

    def start(self):
    
        self.show()
    
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
    
        self.move(
            geometry.center() - self.rect().center()
        )
    
        self.fade.start()

    # =====================================
    # LOADING
    # =====================================

    def set_progress(self, value, status=None):
        """
        این متد رو دستی و هم‌زمان با هر مرحله‌ی واقعیِ
        لودشدن برنامه صدا بزن (نه با یک تایمر ساختگی).
        هر بار صداش بزنی، progress bar و متن status
        آپدیت میشه و بلافاصله رندر میشه تا واقعاً
        روی صفحه دیده بشه.
        """

        self.value = value

        self.progress.setValue(self.value)

        if status is not None:
            self.status.setText(status)

        # مجبور کن Qt همین الان فریم رو رندر کنه،
        # وگرنه تا برگشتن به event loop چیزی دیده نمیشه
        QApplication.processEvents()

    def finish(self):
        self.set_progress(100, "READY TO PAINT")
        self.close()