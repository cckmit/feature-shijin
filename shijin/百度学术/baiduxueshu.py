from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,xlrd
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(r'../国家药品监督管理局/chromedriver(1).exe')
driver.set_window_size(2000,1000)
driver.get('https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=inject_page&author=%E7%AB%A0%E7%BA%AF%E5%85%89&affiliate=')

# time.sleep(2)
n = 0

# 打开文件
data = xlrd.open_workbook("D:\software\百度下载\百度学术爬取医生名单1.xlsx")

# 查看工作表
data.sheet_names()

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('Sheet3')

doctor = table.col_values(1)
hospital = table.col_values(2)
doctor_hospital = dict(zip(doctor,hospital))
ll = ['章纯光','张立','卢佐鸿','赵文汝','国庆显']

while True:
    for doctor,hospital in doctor_hospital.items():
        n += 1
        print(doctor,hospital)
        print(n)
        driver.find_element_by_xpath('//input[@class="infoInput name_input"]').send_keys(doctor)
        driver.find_element_by_xpath('//input[@class="infoInput institution_input"]').send_keys(hospital)
        driver.find_element_by_xpath('//input[@class="searchFormBtn iconfont icon-search-g"]').click()

        time.sleep(1)
        try:
            name = driver.find_element_by_xpath('//div[@class="searchResultItem firstItem noborderItem"]/div[1]/a[1]').text
            if doctor != name:
                driver.find_element_by_xpath('//input[@class="infoInput name_input"]').clear()
                continue
            aa = driver.find_element_by_xpath('//div[@class="searchResultItem firstItem noborderItem"]/div[1]/a[1]').get_attribute('href')
            driver.get(aa)
            # time.sleep(1)
            ## 医生ID
            scholarID = driver.find_element_by_xpath('//span[@class="p_scholarID_id"]').text
            ## 医生名称
            doctor_name = driver.find_element_by_xpath('//div[@class="p_name"]').text
            ## 所属医院
            hospital_name = driver.find_element_by_xpath('//div[@class="p_affiliate"]').text
            ## 被引频次
            cited_frequency = driver.find_element_by_xpath('//ul[@class="p_ach_wr"]/li[1]/p[2]').text
            ## 成果数
            Number_of_achievements = driver.find_element_by_xpath('//ul[@class="p_ach_wr"]/li[2]/p[2]').text
            ## H指数
            H_index = driver.find_element_by_xpath('//ul[@class="p_ach_wr"]/li[3]/p[2]').text
            ## G指数
            G_index = driver.find_element_by_xpath('//ul[@class="p_ach_wr"]/li[4]/p[2]').text
            try:
                ## 领域
                field = driver.find_element_by_xpath('//span[@class="person_domain person_text"]/a').text
                ## 期刊
                periodical = driver.find_element_by_xpath('//div[@class="pie_map_wrapper"]/div[1]/div/p[1]').text
                ## 会议
                conference = driver.find_element_by_xpath('//div[@class="pie_map_wrapper"]/div[2]/div/p[1]').text
                ## 专著
                monograph = driver.find_element_by_xpath('//div[@class="pie_map_wrapper"]/div[3]/div/p[1]').text
                ## 其它
                other = driver.find_element_by_xpath('//div[@class="pie_map_wrapper"]/div[4]/div/p[1]').text
            except:
                pass
            try:
                ## 合作机构1
                cooperative_institution1 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[1]/span[1]/span').text
                ## 合作次数1
                cooperative_number1 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[1]/span[2]/span[2]').text
                ## 合作机构2
                cooperative_institution2 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[2]/span[1]/span').text
                ## 合作次数2
                cooperative_number2 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[2]/span[2]/span[2]').text
                ## 合作机构3
                cooperative_institution3 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[3]/span[1]/span').text
                ## 合作次数3
                cooperative_number3 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[3]/span[2]/span[2]').text
                ## 合作机构4
                cooperative_institution4 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[4]/span[1]/span').text
                ## 合作次数4
                cooperative_number4 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[4]/span[2]/span[2]').text
                ## 合作机构5
                cooperative_institution5 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[5]/span[1]/span').text
                ## 合作次数5
                cooperative_number5 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[5]/span[2]/span[2]').text
                ## 合作机构6
                cooperative_institution6 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[6]/span[1]/span').text
                ## 合作次数6
                cooperative_number6 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[6]/span[2]/span[2]').text
                ## 合作机构7
                cooperative_institution7 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[7]/span[1]/span').text
                ## 合作次数7
                cooperative_number7 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[7]/span[2]/span[2]').text
                ## 合作机构8
                cooperative_institution8 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[8]/span[1]/span').text
                ## 合作次数8
                cooperative_number8 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[8]/span[2]/span[2]').text
                ## 合作机构9
                cooperative_institution9 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[9]/span[1]/span').text
                ## 合作次数9
                cooperative_number9 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[9]/span[2]/span[2]').text
                ## 合作机构10
                cooperative_institution10 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[10]/span[1]/span').text
                ## 合作次数10
                cooperative_number10 = driver.find_element_by_xpath('//ul[@class="co_affiliate_list"]/li[10]/span[2]/span[2]').text
            except NoSuchElementException:
                pass

            try:
                driver.find_element_by_xpath('//div[@class="co_author_wr"]/h3/a').click()
                time.sleep(1)
            except NoSuchElementException:
                driver.back()
                continue


            ## 合作学者1
            cooperative_scholar_name1 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[1]/div').text
            ## 合作学者医院1
            cooperative_scholar_hospital1 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[1]/div').get_attribute('affiliate')
            ## 合作学者次数1
            cooperative_scholar_number1 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[1]/div').get_attribute('paper-count')
            ## 合作学者ID1
            href = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[1]').get_attribute('href')
            driver.get(href)
            cooperative_scholar_scholarID1 = driver.find_element_by_xpath('//span[@class="p_scholarID_id"]').text
            # print(cooperative_scholar_scholarID1)
            driver.back()
            driver.find_element_by_xpath('//div[@class="co_author_wr"]/h3/a').click()
            time.sleep(0.6)

            ## 合作学者2
            cooperative_scholar_name2 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[2]/div').text
            ## 合作学者医院2
            cooperative_scholar_hospital2 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[2]/div').get_attribute('affiliate')
            ## 合作学者次数2
            cooperative_scholar_number2 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[2]/div').get_attribute('paper-count')
            ## 合作学者ID2
            href = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[2]').get_attribute('href')
            driver.get(href)
            cooperative_scholar_scholarID2 = driver.find_element_by_xpath('//span[@class="p_scholarID_id"]').text
            # print(cooperative_scholar_scholarID1)
            driver.back()
            driver.find_element_by_xpath('//div[@class="co_author_wr"]/h3/a').click()
            time.sleep(0.6)

            ## 合作学者3
            cooperative_scholar_name3 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[3]/div').text
            ## 合作学者医院3
            cooperative_scholar_hospital3 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[3]/div').get_attribute('affiliate')
            ## 合作学者次数3
            cooperative_scholar_number3 = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[3]/div').get_attribute('paper-count')
            ## 合作学者ID3
            href = driver.find_element_by_xpath('//div[@class="co_relmap_wrapper"]/a[3]').get_attribute('href')
            driver.get(href)
            cooperative_scholar_scholarID3 = driver.find_element_by_xpath('//span[@class="p_scholarID_id"]').text
            # print(cooperative_scholar_scholarID1)
            driver.back()
            # driver.find_element_by_xpath('//div[@class="co_author_wr"]/h3/a').click()
            # time.sleep(0.5)

            print(doctor,scholarID,doctor_name,hospital_name,cited_frequency,Number_of_achievements,H_index,G_index,field,periodical,conference,monograph,other,
                cooperative_institution1,cooperative_number1,cooperative_institution2,cooperative_number2,
            cooperative_scholar_name1,cooperative_scholar_hospital1,cooperative_scholar_number1,cooperative_scholar_scholarID1)
            # time.sleep(1)
            driver.back()
            # time.sleep(1)
            driver.find_element_by_xpath('//input[@class="infoInput name_input"]').clear()
        except NoSuchElementException:
            driver.find_element_by_xpath('//input[@class="infoInput name_input"]').clear()


        # if n == 5:
        #     os._exit()

# ## 合作学者1
# cooperative_scholar_name1 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[1]/span/p[1]/a').text
# ## 合作学者医院1
# cooperative_scholar_hospital1 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[1]/span/p[2]/span').text
# ## 合作学者2
# cooperative_scholar_name2 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[2]/span/p[1]/a').text
# ## 合作学者医院2
# cooperative_scholar_hospital2 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[2]/span/p[2]/span').text
# ## 合作学者3
# cooperative_scholar_name3 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[3]/span/p[1]/a').text
# ## 合作学者医院3
# cooperative_scholar_hospital3 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[3]/span/p[2]/span').text
# ## 合作学者4
# cooperative_scholar_name4 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[4]/span/p[1]/a').text
# ## 合作学者医院4
# cooperative_scholar_hospital4 = driver.find_element_by_xpath('//div[@class="co_author_wr"]/div/div[4]/span/p[2]/span').text