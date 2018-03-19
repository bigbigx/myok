import os
from appium import webdriver

apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 获取当前项目的根路径

desired_caps = {}
desired_caps['platformName'] = 'Android'  # 设备系统
desired_caps['platformVersion'] = '6.0.1'  # 设备系统版本
desired_caps['deviceName'] = 'KIW-AL10'  # 设备名称
# 测试apk包的路径
desired_caps['app'] = apk_path + '\\app\\shoujibaidu.apk'
# 应用程序的包名
# desired_caps['appPackage'] = 'com.baidu.searchbox'　　
# desired_caps['appActivity'] = 'com.baidu.searchbox.SplashActivity'
# 如果设置的是app包的路径，则不需要配appPackage和appActivity，同理反之

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)  # 启动app
