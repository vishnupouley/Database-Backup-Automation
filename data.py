from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from send_mail import send_mail, decrypt_message

try:
    # Initialize the browser
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    # Open the webpage
    url = 'http://216.10.240.149:8880/login_up.php?success_redirect_url=%2Fadmin%2Fcustomer%2Flist'  # Replace with the actual URL
    driver.get(url)

    # Find and input login credentials
    username = driver.find_element(By.NAME, 'login_name')
    password = driver.find_element(By.NAME, 'passwd')
    login_button = driver.find_element(By.XPATH, "//button[@name='send']")

    passwd = decrypt_message(file='passwd.txt') # Change the file name if changed

    username.send_keys('m******r')
    password.send_keys(passwd)
    # password.send_keys(Keys.RETURN)
    login_button.click()

    print("Login successful!")

except Exception as e:
    print('Login Error:', str(e))
    result = send_mail(status={'':[False, str(e)]})
    time.sleep(5)
    if(result):
        print("Send Failure Mail")
    else:
        print("failed send")

try:
    # Wait for the page to load
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "customers-list-table")))
    print("Customer Page loaded!")
    # Navigate to the form page
    url_task = "http://216.10.240.149:8880/admin/customer/login/id/1191/all/true/"
    driver.get(url_task)

    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pul-alert pul-alert--warning pul-status-message pul-status-message--warning dynamic-list-banner']")))
        print("Mazenet Customer Page loaded!")
        # Navigate to the form page
        url_task = "http://216.10.240.149:8880/smb/database/list/domainId/3277"
        driver.get(url_task)

        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='active-list active-list-collapsible']")))
            print("Database Page loaded!")

            id_num_dict = {
                            "2580": "db1.zip",
                            "6123": "db2.zip",
                            "2689": "db3.zip",
                            "2570": "db4.zip",
                            "2579": "db5.zip",
                            "5909": "db6.zip",
                        }

            status = {}

            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span//a[@class='download-link']")))
                download_link = driver.find_element(By.XPATH,"//span//a[@class='download-link']")
                while(download_link):
                    print("Download link found!")
                    cancel_button = driver.find_element(By.XPATH,"//button[@class='pul-button pul-button--ghost pul-button--empty pul-button--on-dark pul-toast__close']")
                    cancel_button.click()
                    time.sleep(2)
                    download_link = driver.find_element(By.XPATH,"//span//a[@class='download-link']")

            except Exception as e:
                pass

            for id_num, value in id_num_dict.items():

                try:
                    # print(f"{value} - {id_num}")
                    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, f"//div[@id='active-list-item-{id_num}']//div//div//div//div//div//div//div//ul//li//a[@data-action-name='downloadDump' and @class='tool-block']")))
                    export_btn = driver.find_element(By.XPATH, f"//div[@id='active-list-item-{id_num}']//div//div//div//div//div//div//div//ul//li//a[@data-action-name='downloadDump' and @class='tool-block']")
                    export_btn.click()
                    print("Export Dump Clicked!")
                    time.sleep(5)

                    try:
                        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='checkbox']")))
                        checkbox_check = driver.find_element(By.XPATH, "//input[@type='checkbox']")
                        checkbox_check.click()
                        print("Automatic Download checked")

                        try:
                            time.sleep(5)
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']")))
                            submitBtn = driver.find_element(By.XPATH,"//button[@type='submit']")
                            if (submitBtn):
                                submitBtn.click()
                                print("submitted")
                            time.sleep(5)

                            try:
                                time.sleep(40)
                                WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span//a[@class='download-link']")))
                                download_link = driver.find_element(By.XPATH,"//span//a[@class='download-link']")
                                time.sleep(10)

                                if(download_link):
                                    status[value] = [True, None]
                                    time.sleep(5)
                                    print(f"{value} downloaded successfully")
                                cancel_button = driver.find_element(By.XPATH,"//button[@class='pul-button pul-button--ghost pul-button--empty pul-button--on-dark pul-toast__close']")
                                if(cancel_button):
                                    cancel_button.click()
                                    time.sleep(2)
                                url_task = "http://216.10.240.149:8880/smb/database/list/domainId/3277"
                                driver.get(url_task)

                            except Exception as e:
                                print('Download Error:', str(e))
                                status[value] = [False, str(e)]
                                time.sleep(5)
                                print(f"{value} failed to download")
                                url_task = "http://216.10.240.149:8880/smb/database/list/domainId/3277"
                                driver.get(url_task)

                        except Exception as e:
                            print('Submit Error:', str(e))
                            status[value] = [False, str(e)]
                            time.sleep(5)
                            print(f"{value} failed to download")
                            url_task = "http://216.10.240.149:8880/smb/database/list/domainId/3277"
                            driver.get(url_task)

                    except Exception as e:
                        print('Automatic Download Error:', str(e))
                        status[value] = [False, str(e)]
                        time.sleep(5)
                        print(f"{value} failed to download")
                        url_task = "http://216.10.240.149:8880/smb/database/list/domainId/3277"
                        driver.get(url_task)

                except Exception as e:
                    print('List Page Error:', str(e))
                    status[value] = [False, str(e)]
                    time.sleep(5)
                    print(f"{value} failed to download")
                    url_task = "http://216.10.240.149:8880/smb/database/list/domainId/3277"
                    driver.get(url_task)

            result = send_mail(status=status)
            time.sleep(5)
            if(result):
                print("Send Database Mail")
            else:
                print("failed send")

        except Exception as e:
            print('Database Page Error:', str(e))
            result = send_mail(status={'':[False, str(e)]})
            time.sleep(5)
            if(result):
                print("Send Failure Mail")
            else:
                print("failed send")

    except Exception as e:
        print('Mazenet Customer Page Error:', str(e))
        result = send_mail(status={'':[False, str(e)]})
        time.sleep(5)
        if(result):
            print("Send Failure Mail")
        else:
            print("failed send")

except Exception as e:
    print('Customer Page Error:', str(e))
    result = send_mail(status={'':[False, str(e)]})
    time.sleep(5)
    if(result):
        print("Send Failure Mail")
    else:
        print("failed send")

driver.quit()

# pyinstaller --onefile data.py send_mail.py
