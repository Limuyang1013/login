#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import xlwt

url = 'http://jwc.ecjtu.jx.cn/mis_o/login.php'
datas = {'user': 'jwc',
         'pass': 'jwc',
         'Submit': '%CC%E1%BD%BB'
         }
headers = {'Referer': 'http://jwc.ecjtu.jx.cn/mis_o/login.htm',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }
sessions = requests.session()
response = sessions.post(url, headers=headers, data=datas)
file = xlwt.Workbook(encoding='utf-8')
table = file.add_sheet('achieve')


# 设置Excel样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font

    return style


# 判断是否登陆
def isLogin(num):
    return_code = response.status_code
    if return_code == 200:
        if re.match(r"^\d{14}$", num):
            print('请稍等')
        else:
            print('请输入正确的学号')
        return True
    else:
        return False


# 获取成绩
def getScore(num, pagenum, i, j):
    score_healders = {'Connection': 'keep-alive',
                      'User - Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
                      'Content - Type': 'application / x - www - form - urlencoded',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Content - Length': '69',
                      'Host': 'jwc.ecjtu.jx.cn',
                      'Referer': 'http: // jwc.ecjtu.jx.cn / mis_o / main.php',
                      'Upgrade - Insecure - Requests': '1',
                      'Accept - Language': 'zh - CN, zh;q = 0.8'
                      }
    score_url = 'http://jwc.ecjtu.jx.cn/mis_o/query.php?start=' + str(
        pagenum) + '&job=see&=&Name=&Course=&ClassID=&Term=&StuID=' + num
    score_data = {'Name': '',
                  'StuID': num,
                  'Course': '',
                  'Term': '',
                  'ClassID': '',
                  'Submit': '%B2%E9%D1%AF'
                  }

    score_response = sessions.post(score_url, data=score_data, headers=score_healders)
    # 输出到文本
    with open('text.txt', 'wb') as f:
        f.write(score_response.content)
    content = score_response.content
    soup = BeautifulSoup(content, 'html.parser')
    target = soup.findAll('tr')
    try:
        for tag in target[1:]:
            tds = tag.findAll('td')
            j = 0
            # 学期
            semester = str(tds[0].string)
            if semester == 'None':
                break
            else:
                print(semester.ljust(6) + '\t\t\t', end='')
                table.write(i, j, semester, set_style('Arial', 220))
            # 学号
            studentid = tds[1].string
            print(studentid.ljust(14) + '\t\t\t', end='')
            j += 1
            table.write(i, j, studentid, set_style('Arial', 220))
            table.col(i).width = 256 * 16
            # 姓名
            name = tds[2].string
            print(name.ljust(3) + '\t\t\t', end='')
            j += 1
            table.write(i, j, name, set_style('Arial', 220))
            # 课程
            course = tds[3].string
            print(course.ljust(20, ' ') + '\t\t\t', end='')
            j += 1
            table.write(i, j, course, set_style('Arial', 220))
            # 课程要求
            requirments = tds[4].string
            print(requirments.ljust(10, ' ') + '\t\t', end='')
            j += 1
            table.write(i, j, requirments, set_style('Arial', 220))
            # 学分
            scredit = tds[5].string
            print(scredit.ljust(2, ' ') + '\t\t', end='')
            j += 1
            table.write(i, j, scredit, set_style('Arial', 220))
            # 成绩
            achievement = tds[6].string
            print(achievement.ljust(2) + '\t\t', end='')
            j += 1
            table.write(i, j, achievement, set_style('Arial', 220))
            # 重考一
            reexaminef = tds[7].string
            print(reexaminef.ljust(2) + '\t\t', end='')
            j += 1
            table.write(i, j, reexaminef, set_style('Arial', 220))
            # 重考二
            reexamines = tds[8].string
            print(reexamines.ljust(2) + '\t\t')
            j += 1
            table.write(i, j, reexamines, set_style('Arial', 220))
            i += 1
    except:
        print('出了一点小Bug')

    file.save('demo.xls')
    # 总的记录条数,一页显示30条
    # center = soup.findAll('center')
    # countpage = center[1]


if __name__ == '__main__':
    num = input('请输入你的学号：')
    if isLogin(num):
        getScore(num, pagenum=0, i=0, j=0)
        getScore(num, pagenum=1, i=31, j=0)
        getScore(num, pagenum=2, i=61, j=0)
