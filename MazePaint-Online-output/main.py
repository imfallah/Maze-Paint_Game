import sys
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QMessageBox,
    QGraphicsDropShadowEffect,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
)
from splash_screen import SplashScreen
from PyQt5.QtWidgets import QLineEdit, QDialog
from PyQt5.QtCore import (
    Qt,
    QPoint,
    QPointF,
    QUrl,
    QRectF,
    QPropertyAnimation,
    QEasingCurve,
    pyqtProperty,
)
from PyQt5.QtGui import (
    QFont,
    QDesktopServices,
    QPainter,
    QColor,
    QLinearGradient,
    QRadialGradient,
    QPen,
    QPainterPath,
)


from game.pygame_widget import PygameWidget
from game.save_manager import SaveManager
from game.pygame_widget import PygameWidget
from game.save_manager import SaveManager
from game.leaderboard_api import LeaderboardAPI

# Put your real profile links here.
GITHUB_URL = "https://github.com/YOUR_USERNAME"
LINKEDIN_URL = "https://www.linkedin.com/in/YOUR_USERNAME/"


STYLE = """
QMainWindow {
    background: #101218;
}

QWidget {
    background: #101218;
    color: #F2F4F8;
    font-family: DejaVu Sans;
}

QWidget#Header {
    background: #171A22;
    border-bottom: 1px solid #292E39;
}

QWidget#TitleBar {
    background: #171A22;
    border-bottom: 1px solid #292E39;
}

QLabel#TitleBarLabel {
    color: #8F96A5;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
}

QPushButton#TitleBarButton {
    background: transparent;
    border: none;
    color: #8F96A5;
    font-size: 15px;
    font-weight: 700;
    border-radius: 7px;
    min-width: 34px;
    max-width: 34px;
    min-height: 26px;
    max-height: 26px;
    padding: 0px;
}

QPushButton#TitleBarButton:hover {
    background: #222733;
    color: #F2F4F8;
}

QPushButton#CloseBarButton {
    background: transparent;
    border: none;
    color: #8F96A5;
    font-size: 15px;
    font-weight: 700;
    border-radius: 7px;
    min-width: 34px;
    max-width: 34px;
    min-height: 26px;
    max-height: 26px;
    padding: 0px;
}

QPushButton#CloseBarButton:hover {
    background: #E35C62;
    color: #171A22;
}

QLabel#Logo {
    color: #62E38A;
    font-size: 42px;
    font-weight: 900;
}

QLabel#Subtitle {
    color: #8F96A5;
    font-size: 15px;
}

QLabel#PageTitle {
    color: #F2F4F8;
    font-size: 30px;
    font-weight: 800;
}

QLabel#LevelLabel {
    color: #F2F4F8;
    font-size: 18px;
    font-weight: 800;
}

QPushButton {
    background: #222733;
    color: #F2F4F8;
    border: 1px solid #303746;
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 15px;
    font-weight: 700;
}

QPushButton:hover {
    background: #2A3040;
    border-color: #62E38A;
}

QPushButton:pressed {
    background: #1D222D;
}

QLabel#VersionLabel {
    color: #4C5262;
    font-size: 12px;
}

QLabel#ProgressCaption {
    color: #8F96A5;
    font-size: 13px;
    font-weight: 700;
}

QLabel#ProgressValue {
    color: #F2F4F8;
    font-size: 13px;
    font-weight: 800;
}

QProgressBar#LevelProgress {
    background: #1A1E27;
    border: 1px solid #2A2F3B;
    border-radius: 7px;
    min-height: 10px;
    max-height: 10px;
}

QProgressBar#LevelProgress::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #62E38A, stop:1 #45C4A0);
    border-radius: 6px;
}

QPushButton#IconButton {
    background: #222733;
    border: 1px solid #303746;
    border-radius: 12px;
    font-size: 22px;
    padding: 5px;
    min-width: 42px;
    max-width: 42px;
    min-height: 42px;
    max-height: 42px;
}

QPushButton#IconButton:hover {
    background: #303747;
    border-color: #62E38A;
}

QPushButton#BackButton {
    background: transparent;
    border: none;
    color: #8F96A5;
}

QPushButton#BackButton:hover {
    color: #62E38A;
}



QComboBox#LevelCombo {
    background: #222733;
    color: #F2F4F8;
    border: 1px solid #303746;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 14px;
    font-weight: 700;
    min-width: 130px;
}

QComboBox#LevelCombo:hover {
    border-color: #62E38A;
}

QComboBox#LevelCombo QAbstractItemView {
    background: #222733;
    color: #F2F4F8;
    selection-background-color: #303747;
    selection-color: #62E38A;
}

QTableWidget#LeaderboardTable {
    background: #171A22;
    alternate-background-color: #1D222D;
    border: 1px solid #292E39;
    border-radius: 14px;
    gridline-color: #292E39;
    color: #F2F4F8;
    font-size: 14px;
    selection-background-color: #26352D;
    selection-color: #62E38A;
}

QTableWidget#LeaderboardTable::item {
    padding: 10px;
    border-bottom: 1px solid #292E39;
}

QHeaderView::section {
    background: #222733;
    color: #8F96A5;
    border: none;
    padding: 12px;
    font-size: 12px;
    font-weight: 800;
}

QLabel#RankTitle {
    color: #F2F4F8;
    font-size: 16px;
    font-weight: 800;
}

QLabel#MyRank {
    color: #62E38A;
    font-size: 14px;
    font-weight: 800;
}

QLabel#LeaderboardStatus {
    color: #8F96A5;
    font-size: 12px;
}






"""



class UsernameDialog(QDialog):

    def __init__(
        self,
        api,
        parent=None
    ):

        super().__init__(parent)

        self.api = api

        self.setWindowTitle(
            "MazePaint"
        )

        self.setFixedSize(
            420,
            250
        )

        self.setStyleSheet("""
            QDialog {
                background: #171A22;
            }

            QLabel {
                color: #F2F4F8;
            }

            QLineEdit {
                background: #222733;
                color: #F2F4F8;
                border: 1px solid #303746;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border-color: #62E38A;
            }

            QPushButton {
                background: #62E38A;
                color: #101218;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: 900;
            }

            QPushButton:hover {
                background: #7AF09D;
            }
        """)

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            30, 25, 30, 25
        )

        title = QLabel(
            "👤 CREATE YOUR PROFILE"
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 900;
            }
        """)

        title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Choose a username for the World Leaderboard."
        )

        subtitle.setStyleSheet("""
            QLabel {
                color: #8F96A5;
                font-size: 12px;
            }
        """)

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            subtitle
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Username"
        )

        self.input.setMaxLength(
            20
        )

        layout.addWidget(
            self.input
        )

        self.error = QLabel(
            ""
        )

        self.error.setStyleSheet("""
            QLabel {
                color: #FF7657;
                font-size: 11px;
            }
        """)

        layout.addWidget(
            self.error
        )

        button = QPushButton(
            "CONTINUE"
        )

        button.clicked.connect(
            self.accept_username
        )

        layout.addWidget(
            button
        )

    def accept_username(self):

        username = (
            self.input.text()
            .strip()
        )

        if len(username) < 3:

            self.error.setText(
                "Username must contain at least 3 characters."
            )

            return

        if len(username) > 20:

            self.error.setText(
                "Username must be 20 characters or less."
            )

            return

        allowed = (
            username.replace(
                "_",
                ""
            ).isalnum()
        )

        if not allowed:

            self.error.setText(
                "Only letters, numbers and _ are allowed."
            )

            return

        self.api.set_username(
            username
        )

        self.accept()


class TitleBar(QWidget):

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setObjectName("TitleBar")
        self.setFixedHeight(38)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 8, 0)
        layout.setSpacing(6)

        label = QLabel("MAZE PAINT")
        label.setObjectName("TitleBarLabel")
        layout.addWidget(label)

        layout.addStretch()

        minimize = QPushButton("—")
        minimize.setObjectName("TitleBarButton")
        minimize.setCursor(Qt.PointingHandCursor)
        minimize.clicked.connect(self.window.showMinimized)
        layout.addWidget(minimize)

        close = QPushButton("✕")
        close.setObjectName("CloseBarButton")
        close.setCursor(Qt.PointingHandCursor)
        close.clicked.connect(self.window.close)
        layout.addWidget(close)

        self._drag_pos = None

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self._drag_pos = (
                event.globalPos() - self.window.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):

        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.window.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


class MenuButton(QPushButton):
    """
    Self-painted pill-shaped menu button.

    variant="primary"   -> filled accent gradient (PLAY)
    variant="secondary" -> dark outlined card (LEVELS, SETTINGS)

    Hover smoothly lifts the button, brightens its fill and
    (for secondary buttons) fades the border to the accent color.
    """

    ACCENT = QColor(98, 227, 138)

    def __init__(self, icon, text, variant="secondary", parent=None):
        super().__init__(parent)

        self.icon_char = icon
        self.text_label = text
        self.variant = variant

        self._hover = 0.0

        self.setFixedHeight(58 if variant == "primary" else 50)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("QPushButton { background: transparent; border: none; }")

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(98, 227, 138, 0))
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 6)
        self.setGraphicsEffect(self.shadow)

        self.anim = QPropertyAnimation(self, b"hover", self)
        self.anim.setDuration(160)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def _get_hover(self):
        return self._hover

    def _set_hover(self, value):
        self._hover = value

        base_alpha = 130 if self.variant == "primary" else 90
        self.shadow.setColor(QColor(98, 227, 138, int(base_alpha * value)))
        self.shadow.setBlurRadius(6 + 26 * value)
        self.shadow.setOffset(0, 8 - 4 * value)

        self.update()

    hover = pyqtProperty(float, _get_hover, _set_hover)

    def enterEvent(self, event):
        self._animate_to(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_to(0.0)
        super().leaveEvent(event)

    def _animate_to(self, target):
        self.anim.stop()
        self.anim.setStartValue(self._hover)
        self.anim.setEndValue(target)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        margin = 2.0
        lift = 2.5 * self._hover

        rect = QRectF(
            margin,
            margin - lift,
            self.width() - margin * 2,
            self.height() - margin * 2,
        )
        radius = rect.height() / 2

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        if self.variant == "primary":
            gradient = QLinearGradient(rect.topLeft(), rect.topRight())
            gradient.setColorAt(0.0, self.ACCENT.lighter(100 + int(14 * self._hover)))
            gradient.setColorAt(1.0, QColor(58, 190, 150).lighter(100 + int(10 * self._hover)))
            painter.fillPath(path, gradient)
            text_color = QColor(14, 16, 22)
        else:
            base = QColor(28, 34, 44)
            gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
            gradient.setColorAt(0.0, base.lighter(106 + int(14 * self._hover)))
            gradient.setColorAt(1.0, base.darker(108))
            painter.fillPath(path, gradient)

            r = 50 + int((self.ACCENT.red() - 50) * self._hover)
            g = 56 + int((self.ACCENT.green() - 56) * self._hover)
            b = 70 + int((self.ACCENT.blue() - 70) * self._hover)
            pen = QPen(QColor(r, g, b))
            pen.setWidthF(1.2 + 0.8 * self._hover)
            painter.setPen(pen)
            painter.drawPath(path)
            text_color = QColor(242, 244, 248)

        painter.setPen(text_color)
        font = QFont(
            "DejaVu Sans",
            15 if self.variant == "primary" else 14,
            QFont.Black if self.variant == "primary" else QFont.DemiBold,
        )
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self.icon_char}   {self.text_label}")


class SocialButton(QPushButton):
    """Small self-painted pill used for the GitHub / LinkedIn links."""

    ACCENT = QColor(98, 227, 138)

    def __init__(self, icon, text, parent=None):
        super().__init__(parent)

        self.icon_char = icon
        self.text_label = text

        self._hover = 0.0

        self.setFixedSize(148, 42)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("QPushButton { background: transparent; border: none; }")

        self.anim = QPropertyAnimation(self, b"hover", self)
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def _get_hover(self):
        return self._hover

    def _set_hover(self, value):
        self._hover = value
        self.update()

    hover = pyqtProperty(float, _get_hover, _set_hover)

    def enterEvent(self, event):
        self._animate_to(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_to(0.0)
        super().leaveEvent(event)

    def _animate_to(self, target):
        self.anim.stop()
        self.anim.setStartValue(self._hover)
        self.anim.setEndValue(target)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(0, 0, self.width(), self.height())
        radius = rect.height() / 2

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        base = QColor(23, 27, 36)
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0.0, base.lighter(100 + int(20 * self._hover)))
        gradient.setColorAt(1.0, base.darker(104))
        painter.fillPath(path, gradient)

        r = 48 + int((self.ACCENT.red() - 48) * self._hover)
        g = 55 + int((self.ACCENT.green() - 55) * self._hover)
        b = 70 + int((self.ACCENT.blue() - 70) * self._hover)
        pen = QPen(QColor(r, g, b))
        pen.setWidthF(1.0 + 0.4 * self._hover)
        painter.setPen(pen)
        painter.drawPath(path)

        text_color = QColor(185, 192, 204)
        text_color = QColor(
            int(185 + (255 - 185) * self._hover),
            int(192 + (255 - 192) * self._hover),
            int(204 + (255 - 204) * self._hover),
        )
        painter.setPen(text_color)
        font = QFont("DejaVu Sans", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self.icon_char}  {self.text_label}")

class MainMenu(QWidget):

    def __init__(self, window):
        super().__init__()

        #self.window = window
        self.main_window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 45, 80, 35)
        layout.setSpacing(16)


        logo = QLabel("MAZE")
        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""
            QLabel {
                color: #62E38A;
                font-size: 58px;
                font-weight: 900;
                letter-spacing: 8px;
            }
        """)

        layout.addWidget(logo)

        paint = QLabel("PAINT")
        paint.setAlignment(Qt.AlignCenter)

        paint.setStyleSheet("""
            QLabel {
                color: #F2F4F8;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 10px;
            }
        """)

        layout.addWidget(paint)

        subtitle = QLabel("Paint every corridor.")
        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 18px;
            }
        """)

        layout.addWidget(subtitle)

        play = MenuButton(
            "▶",
            "PLAY",
            variant="primary"
        )

        play.clicked.connect(
            lambda: self.main_window.show_game(1)
        )

        layout.addWidget(play)

        # =========================================================
        # LEVELS
        # =========================================================

        levels = MenuButton(
            "▦",
            "LEVELS",
            variant="secondary"
        )

        levels.clicked.connect(
            self.main_window.show_levels
        )

        layout.addWidget(levels)

        # =========================================================
        # LEADERBOARD
        # =========================================================
        profile = MenuButton("👤", "PROFILE", variant="secondary")
        #profile.clicked.connect(self.main_window.show_profile)
        profile.clicked.connect(self.main_window.show_profile)
        layout.addWidget(profile)

        
        leaderboard = MenuButton(
            "🏆",
            "LEADERBOARD",
            variant="secondary"
        )

        leaderboard.clicked.connect(
            self.main_window.show_leaderboard
        )

        layout.addWidget(leaderboard)

        # =========================================================
        # SETTINGS
        # =========================================================

        settings = MenuButton(
            "⚙",
            "SETTINGS",
            variant="secondary"
        )

        settings.clicked.connect(
            self.show_settings
        )

        layout.addWidget(settings)

        # =========================================================
        # SPACER
        # =========================================================

        layout.addStretch()

        # =========================================================
        # SOCIAL BUTTONS
        # =========================================================
        social_layout = QHBoxLayout()
        social_layout.setSpacing(10)



        github = SocialButton(
            "◉",
            "GitHub" 
                )

        github.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/imfallah")
            )
        )

        linkdin = SocialButton(
            "in",
            "LinkedIn"
        )

        linkdin.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://www.linkedin.com/in/imfallah")
            )
        )

        social_layout.addWidget(linkdin)

        layout.addLayout(social_layout)

        version = QLabel("Created By Mohammad • v1.0")
        version.setAlignment(Qt.AlignCenter)
        version.setObjectName("VersionLabel")
        layout.addWidget(version)

        social_layout.addWidget(github) 
        social_layout.addWidget(linkdin)
        layout.addLayout(social_layout)


        # =========================================================
        # VERSION
        # =========================================================

        version = QLabel("MazePaint  •  v1.0")
        version.setAlignment(Qt.AlignCenter)

        version.setStyleSheet("""
            QLabel {
                color: #4F5665;
                font-size: 11px;
                font-weight: 700;
                margin-top: 8px;
            }
        """)

        layout.addWidget(version)

    # =============================================================
    # SETTINGS
    # =============================================================

    def show_settings(self):
        QMessageBox.information(
            self,
            "Settings",
            "Settings panel is coming soon."
        )

class LevelCard(QPushButton):
    """
    Self-painted level-select card.

    Hover behaviour is driven by an animated ``hover`` property
    (0.0 -> 1.0) that smoothly:
      - lifts the card up a few pixels
      - fades in an accent-colored border
      - grows a soft glow (via QGraphicsDropShadowEffect)
      - brightens the background gradient
    """

    ACCENT = QColor(98, 227, 138)

    def __init__(self, level, unlocked, stars, is_next=False, parent=None):
        super().__init__(parent)

        self.level = level
        self.unlocked = unlocked
        self.stars = stars
        self.is_next = is_next
        self.is_hard = level >= 21

        self._hover = 0.0

        self.setFixedSize(136, 98)
        self.setEnabled(unlocked)
        self.setCursor(Qt.PointingHandCursor if unlocked else Qt.ArrowCursor)
        self.setFlat(True)
        self.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.setToolTip(f"Level {level}" if unlocked else "Locked")

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QColor(98, 227, 138, 0))
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 6)
        self.setGraphicsEffect(self.shadow)

        self.anim = QPropertyAnimation(self, b"hover", self)
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    # --- animated property -------------------------------------------------

    def _get_hover(self):
        return self._hover

    def _set_hover(self, value):
        self._hover = value

        alpha = int(110 * value)
        if self.is_hard:
            self.shadow.setColor(QColor(255, 105, 70, alpha))
        else:
            self.shadow.setColor(QColor(98, 227, 138, alpha))
        self.shadow.setBlurRadius(6 + 26 * value)
        self.shadow.setOffset(0, 8 - 4 * value)

        self.update()

    hover = pyqtProperty(float, _get_hover, _set_hover)

    # --- hover events --------------------------------------------------

    def enterEvent(self, event):
        if self.unlocked:
            self._animate_to(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_to(0.0)
        super().leaveEvent(event)

    def _animate_to(self, target):
        self.anim.stop()
        self.anim.setStartValue(self._hover)
        self.anim.setEndValue(target)
        self.anim.start()

    # --- painting --------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        margin = 7.0
        lift = 4.0 * self._hover

        rect = QRectF(
            margin,
            margin - lift,
            self.width() - margin * 2,
            self.height() - margin * 2,
        )

        radius = 18
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # --- background fill ---
        if not self.unlocked:
            base = QColor(21, 24, 32)
        elif self.is_hard:
            base = QColor(48, 28, 30) if self.stars < 3 else QColor(62, 31, 31)
        else:
            base = QColor(22, 55, 40)

        hover_amount = int(16 * self._hover)
        # gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        # gradient.setColorAt(0.0, base.lighter(108 + int(14 * self._hover)))
        # gradient.setColorAt(1.0, base.darker(108))
        # painter.fillPath(path, gradient)

        gradient = QLinearGradient(
            rect.topLeft(),
            rect.bottomRight()
        )

        gradient.setColorAt(
            0.0,
            base.lighter(105 + hover_amount)
        )

        gradient.setColorAt(
            1.0,
            base.darker(108 - int(5 * self._hover))
        )

        painter.fillPath(path, gradient)

        # --- border ---
        if not self.unlocked:
            # Locked
            border_color = QColor(38, 44, 56)
            border_width = 1.0

        elif self.is_hard:
            # Hard levels
            border_color = QColor(
                255,
                103 + int(70 * self._hover),
                74 + int(35 * self._hover)
            )
            border_width = 1.6 + 1.0 * self._hover

        elif self.is_next:
            # Next level
            border_color = QColor(
                self.ACCENT.red(),
                self.ACCENT.green(),
                self.ACCENT.blue(),
                210 + int(45 * self._hover)
            )
            border_width = 2.2

        else:
            # Normal levels
            normal_border = QColor(43, 91, 65)

            r = normal_border.red() + int(
                (self.ACCENT.red() - normal_border.red()) * self._hover
            )

            g = normal_border.green() + int(
                (self.ACCENT.green() - normal_border.green()) * self._hover
            )

            b = normal_border.blue() + int(
                (self.ACCENT.blue() - normal_border.blue()) * self._hover
            )

            border_color = QColor(r, g, b)
            border_width = 1.2 + 1.2 * self._hover

        # Draw border
        pen = QPen(border_color)
        pen.setWidthF(border_width)
        painter.setPen(pen)
        painter.drawPath(path)

        # =========================================================
        # RED HATCH - LOCKED HARD MODE
        # =========================================================

        hard_locked = self.property("hard_locked") is True

        if self.is_hard and hard_locked:

            painter.save()

            # فقط داخل کارت
            painter.setClipPath(path)

            hatch_pen = QPen(QColor(255, 70, 70, 115))
            hatch_pen.setWidthF(1.4)
            painter.setPen(hatch_pen)

            spacing = 14

            # هاشور مورب
            start_x = int(rect.left() - rect.height())
            end_x = int(rect.right() + rect.height())

            x = start_x

            while x <= end_x:

                painter.drawLine(
                    QPointF(x, rect.bottom()),
                    QPointF(x + rect.height(), rect.top())
                )

                x += spacing

            painter.restore()

            # =========================================================
            # BORDER
            # =========================================================

            # Hard locked → قرمز
            border_color = QColor(255, 70, 70, 210)
            border_width = 1.8

            pen = QPen(border_color)
            pen.setWidthF(border_width)

            painter.setPen(pen)
            painter.drawPath(path)

        # --- level number ---
        if self.unlocked:
            painter.setPen(QColor(242, 244, 248))
        else:
            painter.setPen(QColor(90, 97, 112))

        number_font = QFont("DejaVu Sans", 21, QFont.Black)
        painter.setFont(number_font)
        number_rect = QRectF(rect.x(), rect.y() + 10, rect.width(), 34)
        painter.drawText(number_rect, Qt.AlignCenter, f"{self.level:02d}")

        # --- bottom row: stars or lock ---
        if not self.unlocked:
            lock_font = QFont("DejaVu Sans", 15)
            painter.setFont(lock_font)
            painter.setPen(QColor(75, 82, 96))
            lock_rect = QRectF(rect.x(), rect.bottom() - 32, rect.width(), 24)
            painter.drawText(lock_rect, Qt.AlignCenter, "🔒")
        else:
            stars_text = "★" * self.stars + "☆" * (3 - self.stars)
            painter.setPen(
                QColor(255, 199, 89) if self.stars > 0 else QColor(88, 95, 110)
            )
            star_font = QFont("DejaVu Sans", 13)
            painter.setFont(star_font)
            star_rect = QRectF(rect.x(), rect.bottom() - 30, rect.width(), 22)
            painter.drawText(star_rect, Qt.AlignCenter, stars_text)

        # --- "next level" pill ---
        if self.is_next:
            pill_font = QFont("DejaVu Sans", 7, QFont.Bold)
            painter.setFont(pill_font)
            pill_w, pill_h = 40, 15
            pill_rect = QRectF(
                rect.right() - pill_w - 8, rect.top() + 6, pill_w, pill_h
            )
            pill_path = QPainterPath()
            pill_path.addRoundedRect(pill_rect, pill_h / 2, pill_h / 2)
            painter.fillPath(pill_path, self.ACCENT)
            painter.setPen(QColor(16, 18, 24))
            painter.drawText(pill_rect, Qt.AlignCenter, "NEXT")

class LevelSelect(QWidget):

    NORMAL_LEVELS = 20
    HARD_LEVEL_START = 21
    HARD_LEVEL_END = 30

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.save = SaveManager()

        # =========================================================
        # MAIN LAYOUT
        # =========================================================

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # =========================================================
        # HEADER
        # =========================================================

        header = QHBoxLayout()

        back = QPushButton("←  BACK")
        back.setObjectName("BackButton")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.window.show_menu)

        header.addWidget(back)
        header.addStretch()

        title = QLabel("SELECT LEVEL")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)

        header.addWidget(title)
        header.addStretch()

        spacer = QWidget()
        spacer.setFixedWidth(75)
        header.addWidget(spacer)

        layout.addLayout(header)

        # =========================================================
        # PROGRESS
        # =========================================================

        completed = set(
            self.save.data.get("completed", [])
        )

        normal_completed = sum(
            1 for n in range(1, 21)
            if n in completed
        )

        hard_completed = sum(
            1 for n in range(21, 31)
            if n in completed
        )

        total_stars = sum(
            self.save.get_stars(n)
            for n in range(1, 31)
        )

        progress_row = QHBoxLayout()
        progress_row.setSpacing(10)

        caption = QLabel("NORMAL")
        caption.setObjectName("ProgressCaption")
        progress_row.addWidget(caption)

        value = QLabel(
            f"{normal_completed}/20"
        )
        value.setObjectName("ProgressValue")
        progress_row.addWidget(value)

        bar = QProgressBar()
        bar.setObjectName("LevelProgress")
        bar.setTextVisible(False)
        bar.setRange(0, 20)
        bar.setValue(normal_completed)

        progress_row.addWidget(bar, 1)

        stars_caption = QLabel("★ STARS")
        stars_caption.setObjectName("ProgressCaption")
        progress_row.addWidget(stars_caption)

        stars_value = QLabel(
            f"{total_stars}/90"
        )
        stars_value.setObjectName("ProgressValue")
        progress_row.addWidget(stars_value)

        layout.addLayout(progress_row)

        # =========================================================
        # SECTION LABEL
        # =========================================================

        def section_label(text_value, accent=False):

            label = QLabel(text_value)
            label.setObjectName("ProgressCaption")

            if accent:
                label.setStyleSheet("""
                    QLabel {
                        color: #FF7657;
                        font-size: 14px;
                        font-weight: 900;
                    }
                """)

            return label

        # =========================================================
        # SCROLL AREA
        # =========================================================

        from PyQt5.QtWidgets import QScrollArea

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: #151922;
                width: 8px;
                margin: 4px 0 4px 0;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #303746;
                min-height: 40px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #62E38A;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        content = QWidget()

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(
            10, 5, 10, 15
        )
        content_layout.setSpacing(12)

        # =========================================================
        # NORMAL MODE
        # =========================================================

        content_layout.addWidget(
            section_label("NORMAL MODE")
        )

        normal_grid = QGridLayout()
        normal_grid.setHorizontalSpacing(12)
        normal_grid.setVerticalSpacing(10)
        normal_grid.setContentsMargins(
            0, 0, 0, 0
        )

        # Find next normal level
        next_level = None

        for level in range(1, 21):

            if (
                self.save.is_unlocked(level)
                and self.save.get_stars(level) == 0
            ):
                next_level = level
                break

        # ---------------------------------------------------------
        # 20 NORMAL LEVELS
        # ---------------------------------------------------------

        for index, level in enumerate(
            range(1, 21)
        ):

            unlocked = self.save.is_unlocked(level)

            stars = self.save.get_stars(level)

            card = LevelCard(
                level,
                unlocked,
                stars,
                is_next=(level == next_level),
                parent=self
            )

            # IMPORTANT:
            # Normal levels are NOT Hard Mode
            card.setProperty(
                "hard_mode",
                False
            )

            card.setProperty(
                "hard_locked",
                False
            )

            # Normal cards keep original size
            card.setFixedSize(
                136,
                98
            )

            if unlocked:

                card.clicked.connect(
                    lambda checked=False,
                           lvl=level:
                    self.open_level(lvl)
                )

            row = index // 4
            col = index % 4

            normal_grid.addWidget(
                card,
                row,
                col,
                Qt.AlignCenter
            )

        content_layout.addLayout(
            normal_grid
        )

        # =========================================================
        # HARD MODE HEADER
        # =========================================================

        hard_header = QHBoxLayout()

        hard_title = section_label(
            "🔥 HARD MODE",
            accent=True
        )

        hard_header.addWidget(
            hard_title
        )

        hard_header.addStretch()

        # Check Hard Mode
        hard_unlocked = self.save.is_hard_unlocked()

        if hard_unlocked:

            status = QLabel(
                f"UNLOCKED  •  "
                f"{hard_completed}/10"
            )

            status.setStyleSheet("""
                QLabel {
                    color: #FF9B73;
                    font-size: 13px;
                    font-weight: 800;
                }
            """)

        else:

            status = QLabel(
                "🔒 COMPLETE ALL 20 NORMAL LEVELS"
            )

            status.setStyleSheet("""
                QLabel {
                    color: #777F91;
                    font-size: 12px;
                    font-weight: 800;
                }
            """)

        hard_header.addWidget(status)

        content_layout.addLayout(
            hard_header
        )

        # =========================================================
        # HARD LEVELS
        # =========================================================

        hard_grid = QGridLayout()

        hard_grid.setHorizontalSpacing(12)
        hard_grid.setVerticalSpacing(10)

        hard_grid.setContentsMargins(
            0, 0, 0, 0
        )

        # ---------------------------------------------------------
        # 10 HARD LEVELS
        # ---------------------------------------------------------

        for index, level in enumerate(
            range(21, 31)
        ):

            # If Hard Mode is locked,
            # ALL Hard levels are locked.
            unlocked = hard_unlocked

            stars = self.save.get_stars(level)

            card = LevelCard(
                level,
                unlocked,
                stars,
                is_next=False,
                parent=self
            )

            # This IS Hard Mode
            card.setProperty(
                "hard_mode",
                True
            )

            # 🔴 This controls the red hatch
            card.setProperty(
                "hard_locked",
                not hard_unlocked
            )

            # Hard cards are smaller
            card.setFixedSize(
                120,
                88
            )

            if unlocked:

                card.setToolTip(
                    f"🔥 Hard Level {level}"
                )

                card.clicked.connect(
                    lambda checked=False,
                           lvl=level:
                    self.open_level(lvl)
                )

            else:

                card.setToolTip(
                    "🔒 Complete Level 20 "
                    "to unlock Hard Mode"
                )

            row = index // 4
            col = index % 4

            hard_grid.addWidget(
                card,
                row,
                col,
                Qt.AlignCenter
            )

        content_layout.addLayout(
            hard_grid
        )

        # Bottom spacing
        content_layout.addSpacing(10)

        scroll.setWidget(content)

        layout.addWidget(
            scroll,
            1
        )

    # =============================================================
    # OPEN LEVEL
    # =============================================================

    def open_level(self, level):

        if self.save.is_unlocked(level):
            self.window.show_game(level)

    # =============================================================
    # REFRESH
    # =============================================================

    def refresh(self):

        self.window.show_levels()

class LeaderboardPage(QWidget):

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.api = LeaderboardAPI()
        self.current_level = 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 22, 30, 24)
        layout.setSpacing(16)

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header = QHBoxLayout()

        back = QPushButton("←  BACK")
        back.setObjectName("BackButton")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.window.show_menu)

        header.addWidget(back)
        header.addStretch()

        title = QLabel("🏆 LEADERBOARD")
        title.setObjectName("PageTitle")
        title.setAlignment(Qt.AlignCenter)

        header.addWidget(title)

        header.addStretch()

        refresh = QPushButton("↻  REFRESH")
        refresh.setCursor(Qt.PointingHandCursor)
        refresh.clicked.connect(self.load_scores)

        header.addWidget(refresh)

        layout.addLayout(header)

        # -------------------------------------------------
        # Controls
        # -------------------------------------------------

        controls = QHBoxLayout()
        controls.setSpacing(12)

        level_label = QLabel("LEVEL")
        level_label.setObjectName("ProgressCaption")

        controls.addWidget(level_label)

        self.level_combo = QComboBox()
        self.level_combo.setObjectName("LevelCombo")

        for level in range(1, 31):
            if level <= 20:
                self.level_combo.addItem(
                    f"Level {level:02d}",
                    level
                )
            else:
                self.level_combo.addItem(
                    f"🔥 Hard {level:02d}",
                    level
                )

        self.level_combo.currentIndexChanged.connect(
            self.level_changed
        )

        controls.addWidget(self.level_combo)

        controls.addStretch()

        self.status = QLabel("Loading...")
        self.status.setObjectName("LeaderboardStatus")
        controls.addWidget(self.status)

        layout.addLayout(controls)

        # -------------------------------------------------
        # My rank
        # -------------------------------------------------

        self.my_rank = QLabel("")
        self.my_rank.setObjectName("MyRank")
        self.my_rank.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.my_rank)

        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        self.table = QTableWidget()
        self.table.setObjectName("LeaderboardTable")

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "RANK",
                "PLAYER",
                "TIME",
                "STARS"
            ]
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.verticalHeader().setVisible(False)

        header_view = self.table.horizontalHeader()

        header_view.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header_view.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header_view.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header_view.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        layout.addWidget(self.table, 1)

        # -------------------------------------------------
        # Initial load
        # -------------------------------------------------

        self.load_scores()

    def level_changed(self, index):
        level = self.level_combo.itemData(index)

        if level is None:
            return

        self.current_level = int(level)

        self.load_scores()

    def load_scores(self):

        self.current_level = self.level_combo.currentData()

        self.table.setRowCount(0)

        if not self.api.is_configured():
            self.status.setText(
                "⚠ Leaderboard is not configured"
            )
            self.my_rank.setText("")
            return

        self.status.setText("Loading...")

        QApplication.processEvents()

        scores = self.api.get_top_scores(
            level=self.current_level,
            limit=100
        )

        if not scores:
            self.status.setText(
                "No scores yet"
            )
            self.my_rank.setText(
                "Be the first player on this level! 🚀"
            )
            return

        # Sort locally too, just to guarantee ranking order.
        scores.sort(
            key=lambda x: float(
                x.get("time_seconds", 999999)
            )
        )

        self.table.setRowCount(
            len(scores)
        )

        my_rank = None

        for row, score in enumerate(scores):

            rank = row + 1

            player = score.get(
                "username",
                "Player"
            )

            time_seconds = float(
                score.get(
                    "time_seconds",
                    0
                )
            )

            stars = int(
                score.get(
                    "stars",
                    1
                )
            )

            player_id = score.get(
                "player_id"
            )

            # Rank
            if rank == 1:
                rank_text = "🥇"
            elif rank == 2:
                rank_text = "🥈"
            elif rank == 3:
                rank_text = "🥉"
            else:
                rank_text = str(rank)

            rank_item = QTableWidgetItem(
                rank_text
            )

            rank_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                0,
                rank_item
            )

            # Player
            player_item = QTableWidgetItem(
                str(player)
            )

            self.table.setItem(
                row,
                1,
                player_item
            )

            # Time
            time_item = QTableWidgetItem(
                f"{time_seconds:.2f}s"
            )

            time_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                2,
                time_item
            )

            # Stars
            stars_text = (
                "★" * stars +
                "☆" * (3 - stars)
            )

            stars_item = QTableWidgetItem(
                stars_text
            )

            stars_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                3,
                stars_item
            )

            # Find current player
            if player_id == self.api.player_id:
                my_rank = rank

        self.status.setText(
            f"{len(scores)} players"
        )

        if my_rank is not None:
            self.my_rank.setText(
                f"YOUR RANK  •  #{my_rank}"
            )
        else:
            self.my_rank.setText(
                "You don't have a score on this level yet."
            )

    def refresh(self):
        self.load_scores()



class ChatDialog(QDialog):

    def __init__(
        self,
        api,
        other_player,
        parent=None
    ):
        super().__init__(parent)

        self.api = api
        self.other_player = other_player

        self.other_player_id = other_player.get(
            "player_id",
            ""
        )

        self.other_username = other_player.get(
            "username",
            "Player"
        )

        self.setWindowTitle(
            f"Chat with {self.other_username}"
        )

        self.setMinimumSize(
            520,
            620
        )

        self.setStyleSheet("""
            QDialog {
                background: #101218;
            }

            QLabel {
                color: #F2F4F8;
            }

            QLineEdit {
                background: #171A22;
                color: #F2F4F8;
                border: 1px solid #303746;
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border-color: #62E38A;
            }

            QPushButton {
                background: #222733;
                color: #F2F4F8;
                border: 1px solid #303746;
                border-radius: 10px;
                padding: 10px 16px;
                font-weight: 800;
            }

            QPushButton:hover {
                background: #2A3040;
                border-color: #62E38A;
            }

            QPushButton#SendButton {
                background: #62E38A;
                color: #101218;
                border: none;
                min-width: 70px;
            }

            QPushButton#SendButton:hover {
                background: #7AF09D;
            }

            QListWidget {
                background: #171A22;
                border: 1px solid #292E39;
                border-radius: 14px;
                padding: 10px;
                color: #F2F4F8;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(12)

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        avatar = QLabel("👤")

        avatar.setStyleSheet("""
            QLabel {
                font-size: 25px;
            }
        """)

        header.addWidget(avatar)

        title_layout = QVBoxLayout()

        title = QLabel(
            self.other_username
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 900;
            }
        """)

        title_layout.addWidget(title)

        subtitle = QLabel(
            "Private conversation"
        )

        subtitle.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 11px;
            }
        """)

        title_layout.addWidget(subtitle)

        header.addLayout(title_layout)
        header.addStretch()

        refresh = QPushButton("↻")

        refresh.setFixedSize(
            42,
            42
        )

        refresh.clicked.connect(
            self.load_messages
        )

        header.addWidget(refresh)

        layout.addLayout(header)

        # =====================================================
        # MESSAGES
        # =====================================================

        from PyQt5.QtWidgets import QListWidget

        self.messages = QListWidget()

        self.messages.setSpacing(8)

        layout.addWidget(
            self.messages,
            1
        )

        # =====================================================
        # INPUT
        # =====================================================

        input_layout = QHBoxLayout()

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Write a message..."
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        input_layout.addWidget(
            self.input,
            1
        )

        send = QPushButton(
            "SEND"
        )

        send.setObjectName(
            "SendButton"
        )

        send.clicked.connect(
            self.send_message
        )

        input_layout.addWidget(
            send
        )

        layout.addLayout(
            input_layout
        )

        self.load_messages()

    # =========================================================
    # LOAD MESSAGES
    # =========================================================

    def load_messages(self):

        self.messages.clear()

        messages = self.api.get_messages(
            self.other_player_id,
            limit=100
        )

        for message in messages:

            sender_id = message.get(
                "sender_id"
            )

            text = str(
                message.get(
                    "message",
                    ""
                )
            )

            created_at = str(
                message.get(
                    "created_at",
                    ""
                )
            )

            if sender_id == self.api.player_id:

                prefix = "You"

            else:

                prefix = self.other_username

            item_text = (
                f"{prefix}\n"
                f"{text}"
            )

            item = QListWidgetItem(
                item_text
            )

            if sender_id == self.api.player_id:

                item.setTextAlignment(
                    Qt.AlignRight
                )

            else:

                item.setTextAlignment(
                    Qt.AlignLeft
                )

            self.messages.addItem(
                item
            )

        self.api.mark_conversation_read(
            self.other_player_id
        )

        if self.messages.count() > 0:

            self.messages.scrollToBottom()

    # =========================================================
    # SEND MESSAGE
    # =========================================================

    def send_message(self):

        text = (
            self.input.text()
            .strip()
        )

        if not text:
            return

        result = self.api.send_message(
            self.other_player_id,
            text
        )

        if result:

            self.input.clear()

            self.load_messages()

        else:

            QMessageBox.warning(
                self,
                "Chat Error",
                "Could not send the message."
            )


class PlayerSearchDialog(QDialog):

    def __init__(self, api, parent=None):
        super().__init__(parent)

        self.api = api
        self.selected_player = None

        self.setWindowTitle(
            "Find Player"
        )

        self.setMinimumSize(
            460,
            560
        )

        self.setStyleSheet("""
            QDialog {
                background: #101218;
            }

            QLabel {
                color: #F2F4F8;
            }

            QLineEdit {
                background: #171A22;
                color: #F2F4F8;
                border: 1px solid #303746;
                border-radius: 12px;
                padding: 12px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border-color: #62E38A;
            }

            QPushButton {
                background: #222733;
                color: #F2F4F8;
                border: 1px solid #303746;
                border-radius: 10px;
                padding: 11px 16px;
                font-weight: 800;
            }

            QPushButton:hover {
                background: #2A3040;
                border-color: #62E38A;
            }

            QPushButton#SearchButton {
                background: #62E38A;
                color: #101218;
                border: none;
            }

            QPushButton#SearchButton:hover {
                background: #7AF09D;
            }

            QPushButton#OpenButton {
                background: #62E38A;
                color: #101218;
                border: none;
            }

            QListWidget {
                background: #171A22;
                color: #F2F4F8;
                border: 1px solid #292E39;
                border-radius: 14px;
                padding: 8px;
                font-size: 14px;
            }

            QListWidget::item {
                padding: 14px;
                border-radius: 10px;
            }

            QListWidget::item:hover {
                background: #222733;
            }

            QListWidget::item:selected {
                background: #26352D;
                border: 1px solid #62E38A;
            }
        """)

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(
            14
        )

        # =====================================================
        # HEADER
        # =====================================================

        title = QLabel(
            "👥 FIND A PLAYER"
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 900;
                color: #F2F4F8;
            }
        """)

        layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Search for a player to start a private chat."
        )

        subtitle.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 11px;
            }
        """)

        layout.addWidget(
            subtitle
        )

        # =====================================================
        # SEARCH
        # =====================================================

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Enter username..."
        )

        self.search_input.returnPressed.connect(
            self.search_players
        )

        search_layout.addWidget(
            self.search_input
        )

        search_button = QPushButton(
            "🔎 SEARCH"
        )

        search_button.setObjectName(
            "SearchButton"
        )

        search_button.setCursor(
            Qt.PointingHandCursor
        )

        search_button.clicked.connect(
            self.search_players
        )

        search_layout.addWidget(
            search_button
        )

        layout.addLayout(
            search_layout
        )

        # =====================================================
        # PLAYER LIST
        # =====================================================

        self.players = QListWidget()

        self.players.itemDoubleClicked.connect(
            self.open_selected
        )

        layout.addWidget(
            self.players,
            1
        )

        # =====================================================
        # OPEN CHAT
        # =====================================================

        open_button = QPushButton(
            "💬  OPEN CHAT"
        )

        open_button.setObjectName(
            "OpenButton"
        )

        open_button.setCursor(
            Qt.PointingHandCursor
        )

        open_button.clicked.connect(
            self.open_selected
        )

        layout.addWidget(
            open_button
        )

        # =====================================================
        # INITIAL SEARCH
        # =====================================================

        self.search_players()

    # =========================================================
    # SEARCH PLAYERS
    # =========================================================

    def search_players(self):

        query = (
            self.search_input.text()
            .strip()
        )

        self.players.clear()

        results = self.api.search_players(
            query,
            limit=30
        )

        for player in results:

            username = player.get(
                "username",
                "Player"
            )

            item = QListWidgetItem(
                f"👤  {username}"
            )

            item.setData(
                Qt.UserRole,
                player
            )

            self.players.addItem(
                item
            )

        if not results:

            item = QListWidgetItem(
                "No players found."
            )

            item.setFlags(
                Qt.NoItemFlags
            )

            self.players.addItem(
                item
            )

    # =========================================================
    # OPEN SELECTED PLAYER
    # =========================================================

    def open_selected(self):

        item = self.players.currentItem()

        if item is None:
            return

        player = item.data(
            Qt.UserRole
        )

        if not player:
            return

        self.selected_player = player

        self.accept()








class ProfilePage(QWidget):

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.api = LeaderboardAPI()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            35, 25, 35, 25
        )

        layout.setSpacing(18)

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        back = QPushButton(
            "←  BACK"
        )

        back.setObjectName(
            "BackButton"
        )

        back.setCursor(
            Qt.PointingHandCursor
        )

        back.clicked.connect(
            self.window.show_menu
        )

        header.addWidget(
            back
        )

        header.addStretch()

        title = QLabel(
            "👤 PROFILE"
        )

        title.setObjectName(
            "PageTitle"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        refresh = QPushButton(
            "↻  REFRESH"
        )

        refresh.setCursor(
            Qt.PointingHandCursor
        )

        refresh.clicked.connect(
            self.load_profile
        )

        header.addWidget(
            refresh
        )

        layout.addLayout(
            header
        )

        # =====================================================
        # PLAYER CARD
        # =====================================================

        self.player_card = QWidget()

        self.player_card.setStyleSheet("""
            QWidget {
                background: #171A22;
                border: 1px solid #292E39;
                border-radius: 18px;
            }
        """)

        card_layout = QVBoxLayout(
            self.player_card
        )

        card_layout.setContentsMargins(
            25, 22, 25, 22
        )

        # =====================================================
        # USERNAME
        # =====================================================

        self.username_label = QLabel(
            "👤 Player"
        )

        self.username_label.setStyleSheet("""
            QLabel {
                color: #F2F4F8;
                font-size: 25px;
                font-weight: 900;
            }
        """)

        card_layout.addWidget(
            self.username_label
        )

        # =====================================================
        # PLAYER ID
        # =====================================================

        self.player_id_label = QLabel(
            ""
        )

        self.player_id_label.setStyleSheet("""
            QLabel {
                color: #626A7A;
                font-size: 10px;
            }
        """)

        card_layout.addWidget(
            self.player_id_label
        )

        # =====================================================
        # STATS
        # =====================================================

        stats = QHBoxLayout()

        self.rank_label = self.create_stat(
            "🌍 WORLD RANK",
            "#--"
        )

        self.completed_label = self.create_stat(
            "✓ COMPLETED",
            "0 / 30"
        )

        self.stars_label = self.create_stat(
            "⭐ STARS",
            "0 / 90"
        )

        stats.addWidget(
            self.rank_label
        )

        stats.addWidget(
            self.completed_label
        )

        stats.addWidget(
            self.stars_label
        )

        card_layout.addLayout(
            stats
        )

        layout.addWidget(
            self.player_card
        )

        # =====================================================
        # PLAYER CHAT
        # =====================================================

        chat_section = QWidget()

        chat_section.setStyleSheet("""
            QWidget {
                background: #171A22;
                border: 1px solid #292E39;
                border-radius: 18px;
            }
        """)

        chat_layout = QHBoxLayout(
            chat_section
        )

        chat_layout.setContentsMargins(
            20, 16, 20, 16
        )

        chat_layout.setSpacing(
            15
        )

        # =====================================================
        # CHAT ICON
        # =====================================================

        chat_icon = QLabel(
            "💬"
        )

        chat_icon.setStyleSheet("""
            QLabel {
                font-size: 25px;
                border: none;
                background: transparent;
            }
        """)

        chat_layout.addWidget(
            chat_icon
        )

        # =====================================================
        # CHAT TEXT
        # =====================================================

        chat_text_layout = QVBoxLayout()

        chat_title = QLabel(
            "PLAYER CHAT"
        )

        chat_title.setStyleSheet("""
            QLabel {
                color: #F2F4F8;
                font-size: 14px;
                font-weight: 900;
                border: none;
                background: transparent;
            }
        """)

        chat_text_layout.addWidget(
            chat_title
        )

        chat_subtitle = QLabel(
            "Search for another player and start a private conversation."
        )

        chat_subtitle.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 11px;
                border: none;
                background: transparent;
            }
        """)

        chat_text_layout.addWidget(
            chat_subtitle
        )

        chat_layout.addLayout(
            chat_text_layout,
            1
        )

        # =====================================================
        # OPEN CHAT BUTTON
        # =====================================================

        chat_button = QPushButton(
            "💬  OPEN CHAT"
        )

        chat_button.setCursor(
            Qt.PointingHandCursor
        )

        chat_button.setStyleSheet("""
            QPushButton {
                background: #62E38A;
                color: #101218;
                border: none;
                border-radius: 10px;
                padding: 11px 18px;
                font-size: 11px;
                font-weight: 900;
            }

            QPushButton:hover {
                background: #7AF09D;
            }

            QPushButton:pressed {
                background: #4FD474;
            }
        """)

        chat_button.clicked.connect(
            self.open_player_search
        )

        chat_layout.addWidget(
            chat_button
        )

        layout.addWidget(
            chat_section
        )

        # =====================================================
        # RECORD TITLE
        # =====================================================

        records_title = QLabel(
            "MY RECORDS"
        )

        records_title.setStyleSheet("""
            QLabel {
                color: #F2F4F8;
                font-size: 18px;
                font-weight: 900;
            }
        """)

        layout.addWidget(
            records_title
        )

        # =====================================================
        # RECORD TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setObjectName(
            "LeaderboardTable"
        )

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "LEVEL",
                "TIME",
                "STARS",
                "STATUS"
            ]
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.NoSelection
        )

        self.table.verticalHeader().setVisible(
            False
        )

        table_header = (
            self.table.horizontalHeader()
        )

        table_header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        table_header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        table_header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        table_header.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.table,
            1
        )

        # =====================================================
        # LOAD PROFILE
        # =====================================================

        self.load_profile()

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat(
        self,
        title,
        value
    ):

        widget = QWidget()

        widget.setStyleSheet("""
            QWidget {
                background: #1D222D;
                border: 1px solid #303746;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(
            widget
        )

        layout.setContentsMargins(
            15, 12, 15, 12
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            QLabel {
                color: #737B8D;
                font-size: 10px;
                font-weight: 800;
            }
        """)

        value_label = QLabel(
            value
        )

        value_label.setStyleSheet("""
            QLabel {
                color: #62E38A;
                font-size: 20px;
                font-weight: 900;
            }
        """)

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        widget.value_label = value_label

        return widget

    # =========================================================
    # LOAD PROFILE
    # =========================================================

    def load_profile(self):

        username = (
            self.api.get_username()
            or "Player"
        )

        self.username_label.setText(
            f"👤 {username.upper()}"
        )

        self.player_id_label.setText(
            f"Player ID: {self.api.get_display_id()}"
        )

        if not self.api.is_configured():

            self.rank_label.value_label.setText(
                "#--"
            )

            self.completed_label.value_label.setText(
                "0 / 30"
            )

            self.stars_label.value_label.setText(
                "0 / 90"
            )

            self.load_records({})

            return

        stats = self.api.get_my_stats()

        completed = stats.get(
            "completed",
            0
        )

        stars = stats.get(
            "total_stars",
            0
        )

        self.completed_label.value_label.setText(
            f"{completed} / 30"
        )

        self.stars_label.value_label.setText(
            f"{stars} / 90"
        )

        rank = self.api.get_world_rank()

        if rank is None:

            self.rank_label.value_label.setText(
                "#--"
            )

        else:

            self.rank_label.value_label.setText(
                f"#{rank}"
            )

        self.load_records(
            stats.get(
                "records",
                {}
            )
        )

    # =========================================================
    # RECORD TABLE
    # =========================================================

    def load_records(
        self,
        records
    ):

        self.table.setRowCount(
            30
        )

        for row in range(30):

            level = row + 1

            record = records.get(
                level
            )

            # =================================================
            # LEVEL
            # =================================================

            level_item = QTableWidgetItem(
                f"{level:02d}"
            )

            level_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                0,
                level_item
            )

            # =================================================
            # COMPLETED
            # =================================================

            if record:

                time_value = float(
                    record.get(
                        "time_seconds",
                        0
                    )
                )

                stars = int(
                    record.get(
                        "stars",
                        0
                    )
                )

                time_item = QTableWidgetItem(
                    f"{time_value:.2f}s"
                )

                stars_item = QTableWidgetItem(
                    "★" * stars +
                    "☆" * (3 - stars)
                )

                status_item = QTableWidgetItem(
                    "COMPLETED"
                )

                status_item.setForeground(
                    QColor("#62E38A")
                )

            # =================================================
            # NOT COMPLETED
            # =================================================

            else:

                time_item = QTableWidgetItem(
                    "--"
                )

                stars_item = QTableWidgetItem(
                    "☆☆☆"
                )

                if level == 1:

                    status_item = QTableWidgetItem(
                        "NOT COMPLETED"
                    )

                elif level >= 21:

                    status_item = QTableWidgetItem(
                        "HARD MODE"
                    )

                else:

                    status_item = QTableWidgetItem(
                        "LOCKED / NOT PLAYED"
                    )

            # =================================================
            # ALIGNMENT
            # =================================================

            time_item.setTextAlignment(
                Qt.AlignCenter
            )

            stars_item.setTextAlignment(
                Qt.AlignCenter
            )

            status_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                1,
                time_item
            )

            self.table.setItem(
                row,
                2,
                stars_item
            )

            self.table.setItem(
                row,
                3,
                status_item
            )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        self.load_profile()

    # =========================================================
    # OPEN PLAYER SEARCH
    # =========================================================

    def open_player_search(self):

        dialog = PlayerSearchDialog(
            self.api,
            self
        )

        if dialog.exec_() == QDialog.Accepted:

            if dialog.selected_player:

                chat = ChatDialog(
                    self.api,
                    dialog.selected_player,
                    self
                )

                chat.exec_()





class GamePage(QWidget):

    def __init__(self, window, level=1):
        super().__init__()

        self.window = window
        self.level = level

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setObjectName("Header")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 8, 15, 8)

        back = QPushButton("←")
        back.setObjectName("IconButton")
        back.setCursor(Qt.PointingHandCursor)
        back.clicked.connect(self.go_back)

        header_layout.addWidget(back)

        title = QLabel(f"LEVEL {self.level:02d}")
        title.setObjectName("LevelLabel")
        title.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title, 1)

        restart = QPushButton("↻")
        restart.setObjectName("IconButton")
        restart.setCursor(Qt.PointingHandCursor)

        header_layout.addWidget(restart)

        layout.addWidget(header)

        self.game = PygameWidget(level=self.level, parent=self.window)

        layout.addWidget(self.game, 1)

        restart.clicked.connect(self.game.restart)

    def start(self):
        self.game.start()
        self.game.setFocus()

    def stop(self):
        if self.game:
            self.game.stop()

    def go_back(self):
        self.stop()
        self.window.show_levels()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maze Paint")
        self.resize(1000, 750)
        self.setMinimumSize(800, 600)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet(STYLE)

        # =========================================================
        # CENTRAL WIDGET
        # =========================================================

        central = QWidget()

        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # =========================================================
        # TITLE BAR
        # =========================================================

        self.title_bar = TitleBar(self)
        central_layout.addWidget(self.title_bar)

        # =========================================================
        # STACKED WIDGET
        # =========================================================

        self.stack = QStackedWidget()
        central_layout.addWidget(self.stack, 1)
        self.setCentralWidget(central)

        self.game_page = None

        self.menu = MainMenu(self)
        self.stack.addWidget(self.menu)

        self.level_page = LevelSelect(self)
        self.stack.addWidget(self.level_page)

        self.leaderboard_page = LeaderboardPage(self)
        self.stack.addWidget(self.leaderboard_page)

        self.profile_page = ProfilePage(self)
        self.stack.addWidget(self.profile_page)





        self.stack.setCurrentWidget(self.menu)
    def show_menu(self):

        if self.game_page:
            self.game_page.stop()

        self.stack.setCurrentWidget(self.menu)

    def show_leaderboard(self):
        if self.game_page:
            self.game_page.stop()

        self.leaderboard_page.refresh()

        self.stack.setCurrentWidget(
            self.leaderboard_page
        )

    def show_profile(self):
        self.profile_page.refresh()
        self.stack.setCurrentWidget(self.profile_page)


    def show_levels(self):

        if self.game_page:
            self.game_page.stop()

        old_page = self.level_page

        new_page = LevelSelect(self)

        self.stack.addWidget(new_page)

        self.level_page = new_page

        self.stack.setCurrentWidget(new_page)

        self.stack.removeWidget(old_page)
        old_page.deleteLater()

    def show_game(self, level=1):

        if self.game_page:

            self.game_page.stop()

            self.stack.removeWidget(self.game_page)

            self.game_page.deleteLater()

            self.game_page = None

        self.game_page = GamePage(self, level)

        self.stack.addWidget(self.game_page)

        self.stack.setCurrentWidget(self.game_page)

        self.game_page.start()

    def closeEvent(self, event):

        if self.game_page:
            self.game_page.stop()

        event.accept()


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("Maze Paint")

    app.setFont(
        QFont(
            "DejaVu Sans",
            10
        )
    )

    # ==========================================
    # SPLASH
    # ==========================================

    splash = SplashScreen()

    splash.start()

    splash.set_progress(10, "INITIALIZING...")

    api = LeaderboardAPI()

    splash.set_progress(30, "LOADING MAZE ENGINE...")

    if not api.has_username():

        # موقتاً splash رو کنار می‌زنیم تا دیالوگ دیده بشه
        splash.hide()

        dialog = UsernameDialog(api)

        if dialog.exec_() != QDialog.Accepted:
            splash.close()
            sys.exit(0)

        splash.show()

    splash.set_progress(55, "PREPARING LEVELS...")

    # ==========================================
    # MAIN WINDOW
    # ==========================================

    window = MainWindow()

    splash.set_progress(80, "LOADING PLAYER DATA...")

    # ==========================================
    # ONLINE
    # ==========================================

    online_api = LeaderboardAPI()

    if online_api.get_username():
        online_api.set_username(
            online_api.get_username()
        )

    online_api.start_heartbeat(30)

    window._online_api = online_api

    splash.set_progress(95, "READY TO PAINT")

    # ==========================================
    # SHOW MAIN WINDOW
    # ==========================================

    window.show()

    splash.finish()

    # ==========================================
    # APP LOOP
    # ==========================================

    exit_code = app.exec_()

    online_api.stop_heartbeat()
    online_api.update_online_status(False)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

