import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMessageBox, QFileDialog, QTabWidget, QToolBar, QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, QUrl

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Back", self)
        back_btn.setStatusTip("Back to Previous page")
        navtb.addAction(back_btn)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        next_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        reload_btn = QAction(QIcon(os.path.join('icons', 'cil-reload.png')), "reload", self)
        reload_btn.setStatusTip("reload Page")
        navtb.addAction(reload_btn)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())

        home_btn = QAction(QIcon(os.path.join('icons', 'cil-home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cli-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        stop_btn = QAction(QIcon(os.path.join('icons', 'cil-media-step.png')), "Stop", self)
        navtb.addAction(stop_btn)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        file_menu = self.menuBar().addMenu("&File")
        open_file_action = QAction(QIcon(os.path.join('icons', 'cil-folder-open.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        help_menu = self.menuBar().addMenu("&Help")
        navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')), "Homepage", self)
        navigate_home_action.setStatusTip("Go to spinn Design HomePage")
        help_menu.addAction(navigate_home_action)
        navigate_home_action.triggered.connect(self.navigate_home)

        self.setWindowTitle('browser')
        self.setWindowIcon(QIcon(os.path.join('icons', 'cil-screen-desktop.png')))

        # self.setStyleSheet(QTabWidget{
        # })

        self.add_new_tab(QUrl('http://www.google.com'), 'HomePage')
        self.show()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock.png')))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock.png')))
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(""))

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getenv('HOME'))

        file_extension = os.path.splitext(file_path[0])[1]

        if file_extension in ['.pdf', '.txt', '.html', '.png', '.jpg']:
            self.add_new_tab(QUrl.fromLocalFile(file_path[0]), os.path.basename(file_path[0]))
        else:
            QMessageBox.warning(self, "Extension not supported", "Extension not supported")


app = QApplication(sys.argv)
app.setApplicationName("browser")
app.setOrganizationName("company")
app.setOrganizationDomain("google.com")

window = MainWindow()
app.exec_()



