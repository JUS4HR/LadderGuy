from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
import winreg
import sys

# 点击行为


def onTrayIconActivated(reason):
    if reason == QSystemTrayIcon.DoubleClick:
        switchLadder()

# 切换代理开关


def switchLadder():
    if winreg.QueryValueEx(keyProxy, "ProxyEnable")[0]:
        winreg.SetValueEx(keyProxy, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        setIconTheme()
    else:
        winreg.SetValueEx(keyProxy, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        setIconTheme()

# 设置开机自启动


def autoStart(input):
    if input:
        winreg.SetValueEx(keyStart, "LadderGuy", 0,
                          winreg.REG_SZ, "\"" + sys.executable + "\"")
    else:
        winreg.DeleteValue(keyStart, "LadderGuy")

# 退出函数


def stopApp():
    winreg.CloseKey(keyProxy)
    winreg.CloseKey(keyTheme)
    winreg.CloseKey(keyStart)
    app.quit()

# 根据代理开关状态以及系统亮暗主题设置图标


def setIconTheme():
    iconPath = "ico/"
    # 检查系统亮暗主题
    if winreg.QueryValueEx(keyTheme, "AppsUseLightTheme")[0]:
        iconEnabled = QIcon(iconPath + "ladderIntactDark.ico")
        iconDisabled = QIcon(iconPath + "ladderBrokenDark.ico")
    else:
        iconEnabled = QIcon(iconPath + "ladderIntactLight.ico")
        iconDisabled = QIcon(iconPath + "ladderBrokenLight.ico")
    if winreg.QueryValueEx(keyProxy, "ProxyEnable")[0]:
        tray.setIcon(iconEnabled)
    else:
        tray.setIcon(iconDisabled)


# 用来管理系统代理设置的托盘应用
if __name__ == '__main__':
    # 创建注册表访问对象
    keyProxy = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                              0,
                              winreg.KEY_ALL_ACCESS)
    keyTheme = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                              0,
                              winreg.KEY_ALL_ACCESS)
    keyStart = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                              0,
                              winreg.KEY_ALL_ACCESS)

    # 创建托盘应用
    app = QApplication([])
    app.setApplicationName("梯子大爷")
    app.setApplicationVersion("1.2")
    app.setApplicationDisplayName("梯子大爷")
    app.setQuitOnLastWindowClosed(False)
    # 创建图标
    iconEnabled = QIcon()
    iconDisabled = QIcon()
    tray = QSystemTrayIcon()
    tray.setToolTip("梯子大爷")
    setIconTheme()
    # 创建动作
    actionSwitch = QAction("给我切换梯子", tray)
    actionSwitch.triggered.connect(switchLadder)
    actionSetStartup = QAction("别让我喊", tray)
    actionSetStartup.triggered.connect(autoStart)
    actionSetStartup.setCheckable(True)
    actionStop = QAction("", tray)
    actionStop = QAction("你可以爬了", tray)
    actionStop.triggered.connect(stopApp)
    # 创建菜单
    menu = QMenu()
    menu.addAction(actionSwitch)
    menu.addAction(actionSetStartup)
    menu.addSeparator()
    menu.addAction(actionStop)
    # 设置菜单中的选定框初始状态
    try:
        if winreg.QueryValueEx(keyStart, "LadderGuy")[0]:
            actionSetStartup.setChecked(True)
    except:
        pass
    # 将菜单添加到托盘图标
    tray.setContextMenu(menu)
    tray.setVisible(True)
    # 添加激活行为
    tray.activated.connect(onTrayIconActivated)
    app.exec_()
