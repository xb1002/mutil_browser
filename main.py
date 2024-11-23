from selenium import webdriver
import asyncio
import os

# 创建chrome_data目录，用于存放用户数据
if not os.path.exists('./chrome_data'):
    os.makedirs('./chrome_data')
# 获取./chrome_data的绝对路径
chrome_data_dir = os.path.abspath('./chrome_data')

profile = 'user1'
driver_path = './chromedriver'
extension_paths = [
    './extension/Phantom.crx',
]

async def main():
    user_data_dir = rf"{chrome_data_dir}/{profile}"
    # 如果不存在目录则创建
    if not os.path.exists(user_data_dir):
        print(f"the profile {profile} is not exists, are you sure to create it? ")
        select = input("yes or no(Y/N): ")
        if select.lower() == 'y' or select.lower() == 'yes' or select == '':
            print(f"creating profile {profile}...")
            os.makedirs(user_data_dir)
        else:
            print("exitting...")
            return
    options = webdriver.ChromeOptions()
    # 添加扩展
    for path in extension_paths:
        options.add_extension(path)
    # 添加参数
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # 解决资源限制问题
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument(f"--user-data-dir={user_data_dir}")
    # 取消自动测试提示
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = None
    try:
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        while True:
            await asyncio.sleep(5)
            if not driver.window_handles:
                break
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exitting...")