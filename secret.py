import colorama
import datetime

TOKEN = "NTk3ODM4OTE0MDg2MjQwMzA0.XovONg.vxSl71b9MLwAW0hk2HCz1lBsuGk"

DEV = "test server"
INIT_REQUEST = f"{datetime.datetime.today()} {colorama.Fore.GREEN} [+ EVENT]  [INIT] {colorama.Fore.RESET}"
ERROR_INIT_REQUEST = f"{datetime.datetime.today()} {colorama.Fore.GREEN} [+ EVENT] {colorama.Fore.RED} [ERROR] {colorama.Fore.RESET}"
SUCCESSFUL_REQUEST = f"{datetime.datetime.today()} {colorama.Fore.GREEN} [+ EVENT] %s {colorama.Fore.RESET} %s"
WAITING_REQUEST = f"{datetime.datetime.today()} {colorama.Fore.RED + colorama.Fore.YELLOW} [+ EVENT] %s {colorama.Fore.RESET} %s"
ERROR_REQUEST = f"{datetime.datetime.today()} {colorama.Fore.RED} [+ EVENT] %s {colorama.Fore.RESET} %s"

def dev_or_not(ctx):
    return ctx.guild.name == DEV
