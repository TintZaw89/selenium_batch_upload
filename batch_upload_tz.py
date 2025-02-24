import time, datetime
import os
import shutil
import fnmatch
import re
import maskpass

from itertools import islice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager

myfile = open("Model_ini.txt", "r")
myline = myfile.readline()
str1,str2,str3,str4,str5,str6,str7,str8,str9,str10,str11 = re.sub(r'\s', '', myline).split(',')
myfile.close()

const_mask = "*"
if str8 == '':
    pwd = maskpass.askpass(prompt=f"""User : {str7} 
Password : """, mask=const_mask)
else:
    pwd = str8

str2,str6,str11,str3 = str2.upper(),str6.upper(),str11.upper(),str3.upper()
str_module = 'Recharge' if str2 == 'R' else 'Adjustment'
newfile = str1 + '_' + str_module + '.txt'
newtextfile = str1 + '.txt'
newfile_loop = str1 + '_' + str_module 
module = 'Batch Recharge' if str2 == 'R' else 'Balance Adjust in Batch'

Curr_Directory = os.getcwd()
Upload_Dir = f"{Curr_Directory}\\Upload"

if not os.path.exists(Upload_Dir):
     os.makedirs(Upload_Dir)

if os.path.exists(newtextfile):
    pass
else:
    print(f'The file:{newtextfile} does not exist.') 
    raise SystemExit(0)

str2_txt = "Please input A for Adjustment, R for Recharge at second column"
str3_txt = "Please input (C)Credit for Loan Waive, D for Deduct balance at third column"
str6_txt = "Please input T for Testbed, P for Production at sixth column"
str5_txt = "Please input 1 for Column Name Checking, 0 to operate at fifth column"
str10_txt = "Please input 1 for Export Log file or 0 to skip at 10th column"

def check_col(col_name,value1,value2,out_txt):
    if (col_name != value1) and (col_name != value2):
        print(out_txt)
        raise SystemExit(0)
    
check_col(str2,'A','R',str2_txt)
if str2 == 'A':
    check_col(str3,'C','D',str3_txt)
check_col(str5,'0','1',str5_txt)
check_col(str6, 'T','P', str6_txt)
check_col(str10,'0','1',str10_txt)

check_file = open(newtextfile, "r")
check_line = check_file.readline()
check_file.close()
split_text ='|' if str2 == 'R' else ','
try:
    col1,col2 = check_line.split(split_text,1)
except ValueError:
    print(f"Wrong file! Please use {module} file.")
    raise SystemExit(0)

def get_browser(s):
    if s in ['C', 'E', 'F', 'S']:
        return True                                                       
    return False
    
if get_browser(str11) == False:
    print("Please use F for Firefox, C for Chrome, E for Edge and S for Safari.")
    raise SystemExit(0)
else:
    pass

while True:
    try:
        numb = int(str4)
        if numb < 1 :
            str4 = 1 
        elif numb > 5000:
            str4 = 5000
        else:
            break

    except ValueError:
        print("Error! Numbers only! Please input between 1 and 5000")
        time.sleep(1)
        raise SystemExit(0)

try: #sec_per_batch
    numb = int(str9)
    if str6 == 'T' and (numb < 2 or numb > 300):
        if str2 == 'R':
            str9 = 300
        elif str2 == 'A':
            str9 = 120
    if str6 == 'P': # for production 
        if str2 == 'A' and  str3 == 'C': 
            str9 = 175 # Loan Waive 
        elif str2 == 'A' and  str3 == 'D':
            str9 = 120 # Forfeit
        else:
            str9 = 300 # Recharge

except ValueError:
    print("This is not a number, please input integer only")
    raise SystemExit(0)

web_link = 'https://localhost:8088/portal/' if str6 == 'T' else 'http://localhost:8080/portal/'

sec_per_batch = int(str9)

if str8 != '':
    pwd_count = const_mask * len(str8)
    print(f"User : {str7}\nPassword : {pwd_count}\nSR_NO : {str1}\nModule : {str_module}\nfile_extension : txt\nlines_per_file : {str4}\ncheck_column_name : {str5}\nweb_link : {web_link}\nsec_per_batch : {str9}\nRoot_Path : {Curr_Directory}\n")
else:
    print(f"SR_NO : {str1}\nModule : {str_module}\nfile_extension : txt\nlines_per_file : {str4}\ncheck_column_name : {str5}\nweb_link : {web_link}\nsec_per_batch : {str9}\nRoot_Path : {Curr_Directory}\n")

if str2 == 'R':
    print('NOTICE! Please check cashier to open before recharge process\n')
    time.sleep(3)

if str5 == "0":
    pass
else:
    raise SystemExit(0)

source_dir_file = f"{Curr_Directory}\\{newtextfile}"
target_dir_file = f"{Upload_Dir}\\{newtextfile}"
shutil.move(source_dir_file, target_dir_file)
os.chdir(Upload_Dir)
MyDirectory = os.getcwd()

new_dir = f"{MyDirectory}\\{str1}"
if not os.path.exists(new_dir):
     os.makedirs(new_dir)

copy_source = f"{MyDirectory}\\{newtextfile}"
paste_dest = f"{MyDirectory}\\{str1}\\{newtextfile}"
shutil.copyfile(copy_source, paste_dest)
os.chdir(str1)
os.rename(newtextfile,newfile)

def slice_data(filename):
    lines_per_file = int(str4)
    with open(f"{filename}") as file:
        i = 1
        while True:
            lenth=len(str(i))

            if lenth == 1:
                l = '00'
            elif lenth == 2:
                l = '0'
            else:
                l = ''
            try:
                checker = next(file)
            except StopIteration:
                break
            with open(f"{newfile_loop}_{l}{i}.txt", 'w') as out_file:
                out_file.write(checker)
                for line in islice(file, lines_per_file-1):
                    out_file.write(line)
            i += 1

slice_data(newfile)

temp_dir = f"{MyDirectory}\\{str1}\\temp"
curr_dir = f"{MyDirectory}\\{str1}\\{newfile}"
move_dir = f"{temp_dir}\\{newfile}"
if not os.path.exists(temp_dir):
     os.makedirs(temp_dir)
shutil.move(curr_dir, move_dir)

log_path = f'{Curr_Directory}\\log'
if not os.path.exists(log_path):
     os.makedirs(log_path)

save_path = f'{log_path}\\log-{datetime.datetime.now().strftime("%Y%m%d")}.txt'
if not os.path.exists(save_path):
    # Create new log file if not exist
    with open(save_path, "w") as file:
        file.write("############Log file created!############\n")

def write_data(data):
    with open(save_path, mode='a') as f:
        f.write(data + "\n")

MyUploadDirectory = new_dir # files path need to upload
directory = os.fsencode(MyUploadDirectory)

if str11 == 'F': driver = webdriver.Firefox()
elif str11 == 'C': driver = webdriver.Chrome()
elif str11 == 'E': driver = webdriver.Edge()
else: driver = webdriver.Safari()

driver.get(web_link)
driver.maximize_window()
time.sleep(5)

try: 
    driver.find_element(By.ID,'inputUserName')
    # if link is broken, go back
except TimeoutException:
    time.sleep(20)
    driver.back()

username = driver.find_element(By.ID,'inputUserName')
username.send_keys(str7)#('username')
time.sleep(1)
password = driver.find_element(By.ID,'inputPasswd')
password.send_keys(pwd)#('password')
driver.find_element(By.ID,'btnLogin').click()
time.sleep(7)

try: 
    element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID,'101215')))
    driver.execute_script("arguments[0].click();", element)

    time.sleep(2)
    btn_login = '//button[@type="button" and (contains(@class,"btn-primary")) and(contains(text(),"OK"))]'
    on_click = driver.find_element(By.XPATH, btn_login)

    # if link is broken, go back
except TimeoutException:
    time.sleep(20)
    driver.back()

on_click.click()
time.sleep(10)
wait = WebDriverWait(driver, 10)

span = driver.find_element(By.CLASS_NAME,"iconfont")
span.click()
time.sleep(10)
modulename = driver.find_element(By.ID,'searchMenuInput')
modulename.send_keys(module) #Balance Adjust in Batch || Batch Recharge
time.sleep(3)
driver.find_element(By.ID,'secondThirdMenu-search').click()
time.sleep(5)

print("Start uploading file...")

if (str2 == 'A') and (str6 == 'T'):
    module = 'BatchAdjust'
elif (str2 == 'A') and (str6 == 'P'):
    module = 'Batch Adjust'
else:
    module = 'Batch Recharge'

curr_file_size = 250000
match, my_attached = '',''
warning_popup ='//button[@type="button" and (contains(@class,"btn-warning")) and(contains(text(),"OK"))]'

def upload_attach():
    upload_file = driver.find_element(By.NAME,'uploadFiles')
    upload_file.send_keys(cur_file_name)
            
def is_match():
    attached_element = (r"//div[@class='file-container']//div[@class='row']//div[@class='col-md-12']"
    r"//ul[contains(@class, 'file-list')]//li[@class='list-group-item' and (contains(text(), '.txt'))]")
    my_attached = driver.find_element(By.XPATH, attached_element).text
    match = str.__contains__(my_attached, filename)
    return match

def btn_upload():
    upload_module = '//button[@type="button" and (contains(@class,"btn-primary")) and(contains(text(),"' + module + '"))]'
    upload_btn = driver.find_element(By.XPATH, upload_module) #Batch Recharge #Batch Adjust
    upload_btn.click()

def btn_refresh():
    driver.find_element(By.ID,'btnRefreshMenu').click()

def btn_export_log():
    export_log = '//button[@type="button" and (contains(@class,"btn-default")) and(contains(text(),"Export"))]'
    btn_export = driver.find_element(By.XPATH, export_log)
    btn_export.click()

def update_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for file in os.listdir(directory):
        filename = os.fsdecode(file)
        cur_file_name = f'{MyUploadDirectory}\\{filename}'
        file_stats = os.stat(cur_file_name) 
        cur_loop_file = f'{newfile_loop}'+'_*.txt'
        move_file = f'{temp_dir}\\{filename}'

        if file_stats.st_size < curr_file_size and fnmatch.fnmatch(filename, cur_loop_file):

            upload_attach()
            time.sleep(2)

            try:
                is_match() 
                    
            except NoSuchElementException:
                pass
                btn_refresh()
                time.sleep(2)
                upload_attach()
                time.sleep(2)
         
            if (is_match):
                
                try:
                    btn_upload()

                    try:
                        checkup_click_warning = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, warning_popup)))
                      
                        if (checkup_click_warning.size['height'] > 0) and (checkup_click_warning.size['width'] > 0):
                            actions = webdriver.ActionChains(driver)
                            actions.move_to_element(checkup_click_warning).click().perform()
                            time.sleep(2)
                            btn_upload()
                    
                    except TimeoutException:
                        pass
                       
                except ElementClickInterceptedException:
                    time.sleep(2)
                    element = wait.until(EC.presence_of_element_located(driver.find_element(By.XPATH,warning_popup)))
                    driver.execute_script("arguments[0].click();", element)
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()

                time.sleep(sec_per_batch)# wait next file #100 for Batch Adjust and Batch Recharge

                if str10 == "1":
                    btn_export_log()
                    time.sleep(2)

                btn_refresh()
                log_data = f"{filename} uploaded successfully at " + update_time()
                shutil.move(cur_file_name, move_file)
            
            else:
                log_data = f"{filename}" + " Attached is incorrect"

            print(log_data)
            write_data(log_data)
            time.sleep(2)

print("Upload Process Finished.")
time.sleep(5)
os.remove(copy_source)
driver.quit()