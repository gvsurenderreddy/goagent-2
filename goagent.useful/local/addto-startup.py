#!/usr/bin/env python
# coding:utf-8

from __future__ import with_statement

__version__ = '1.0'

import sys
import os
import re
import time
import ctypes
import platform

# -----------------------------------------------------------------------------
# Add to linux start
# -----------------------------------------------------------------------------
def main_linux():
    filename = os.path.abspath(__file__)
    dirname = os.path.dirname(filename)
    #you can change it to 'proxy.py' if you like :)
    scriptname = 'goagent-gtk.py'
    DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Network;Proxy;
Exec=/usr/bin/env python "%s/%s"
Icon=%s/goagent-logo.png
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=GoAgent GTK
Comment=GoAgent GTK Launcher
''' % (dirname , scriptname , dirname)
    #sometimes maybe  /etc/xdg/autostart , ~/.kde/Autostart/ , ~/.config/openbox/autostart
    for dirname in map(os.path.expanduser, ['~/.config/autostart']):
        if os.path.isdir(dirname):
            filename = os.path.join(dirname, 'goagent-gtk.desktop')
            with open(filename, 'w') as fp:
                fp.write(DESKTOP_FILE)
           # os.chmod(filename, 0755)

# -----------------------------------------------------------------------------
# Add to Macintosh start
# -----------------------------------------------------------------------------
def main_macos():
    if os.getuid() != 0:
        print 'please use sudo run this script'
        sys.exit()
    PLIST = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>GroupName</key>
	<string>wheel</string>
	<key>Label</key>
	<string>org.goagent.macos</string>
	<key>ProgramArguments</key>
	<array>
		<string>/usr/bin/python</string>
		<string>%(dirname)s/proxy.py</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>UserName</key>
	<string>root</string>
	<key>WorkingDirectory</key>
	<string>%(dirname)s</string>
    <key>StandardOutPath</key>
    <string>/var/log/goagent.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/goagent.log</string>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
</dict>
</plist>''' % dict(dirname=os.path.abspath(os.path.dirname(__file__)))
    filename = '/Library/LaunchDaemons/org.goagent.macos.plist'
    print 'write plist to %s' % filename
    with open(filename, 'wb') as fp:
        fp.write(PLIST)
    print 'write plist to %s done' % filename
    print 'Adding CA.crt to system keychain, You may need to input your password...'
    cmd = 'sudo security add-trusted-cert -d -r trustRoot -k "/Library/Keychains/System.keychain" "%s/CA.crt"' % os.path.abspath(os.path.dirname(__file__))
    if os.system(cmd) != 0:
        print 'Adding CA.crt to system keychain Failed!'
        sys.exit(0)
    print 'Adding CA.crt to system keychain Done'
    print 'To start goagent right now, try this command: sudo launchctl load /Library/LaunchDaemons/org.goagent.macos.plist'
    print 'To checkout log file: using Console.app to locate /var/log/goagent.log'

# -----------------------------------------------------------------------------
# Add to Windows start
# -----------------------------------------------------------------------------
def main_windows():
    if 1 == ctypes.windll.user32.MessageBoxW(None, u'是否将goagent.exe加入到启动项？', u'GoAgent 对话框', 1):
        if 1 == ctypes.windll.user32.MessageBoxW(None, u'是否显示托盘区图标？', u'GoAgent 对话框', 1):
            pass

# =============================================================================
# main
# =============================================================================
def main():
    if os.name == 'nt':
        main_windows()
    elif sys.platform == 'darwin':
        main_macos()
    elif sys.platform.startswith('linux'):
        main_linux()
    else:
        pass


if __name__ == '__main__':
   try:
       main()
   except KeyboardInterrupt:
       pass
