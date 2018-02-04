#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import random
import xlsxwriter

def run(keyword):
    # 打开google浏览器
    driver = webdriver.Chrome('chromedriver')

    # 打开网站
    driver.get(
        "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=UUGBXFFZ&guid=b44b2874-4e12-65adb89f-5e94dffa3856&conditions=searchWord+QWJS+++全文检索:" + keyword)
    # 最大化窗口
    driver.maximize_window()
    # 休眠
    url_collect = [];

    while True:
        time.sleep(random.randint(10, 15))
        count = driver.execute_script("return $('.wstitle a').length")
        i = 0

        while i < count:
            code = driver.execute_script("return $($('.wstitle a')[%d]).attr('href')" % i)
            i = i + 2
            url = 'http://wenshu.court.gov.cn' + code
            url_collect.append(url)

        # 如果最后一页执行完毕退出循环
        if driver.execute_script("return $('.current.next').html()") != None:
            break

        # 休眠10s
        time.sleep(random.randint(10, 15))

        # 点击下一页
        elem = driver.find_element_by_class_name("next")
        elem.click()
    print(url_collect)

    res_list = []
    for url in url_collect:
        driver.get(url.replace('contents', 'content'))
        time.sleep(random.randint(10, 15))
        title = driver.execute_script("return $('#contentTitle').text()")
        timer = driver.execute_script("return $('#tdFBRQ').text()").strip()
        content = driver.execute_script("return $('#DivContent').text()")
        j = 2
        while True:
            law_num = driver.execute_script("return $('#DivContent div').eq(%d).text()"%(j,))
            if '号' in law_num:
                break
            else:
                j = j + 1

        time.sleep(random.randint(10, 15))
        list_unit = [title, law_num, timer, content]

        res_list.append(list_unit)
        print(list_unit)
    print(res_list)

    # Create an new Excel file and add a worksheet.
    file_name = '%s-%d.xlsx' % (keyword, random.randint(1000, 9999)) # 文件名称
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    # 添加标题
    worksheet.write('A1', '判决标题')
    worksheet.write('B1', '判决号')
    worksheet.write('C1', '日期')
    worksheet.write('D1', '判决内容')
    # 累加号
    l = 2
    for item in res_list:
        worksheet.write('A%s' % (l,), item[0])
        worksheet.write('B%s' % (l,), item[1])
        worksheet.write('C%s' % (l,), item[2])
        worksheet.write('D%s' % (l,), item[3])
        l = l + 1
    workbook.close()

    # 退出浏览器，close()是关闭当前访问页面，quit()是退出浏览器，结束进程，且回收临时文件
    driver.quit()
    return file_name
