import requests
from bs4 import BeautifulSoup
import re
import crawling
import os
"""
各求人情報を取得する
このとき各配列と変数は以下のように設定する
job_list=各求人情報
job_num=求人番号
job_name=アルバイト募集名
job_tipe=勤務形態
job_point=仕事内容
job_money=最低給与
job_traffic=勤務地
job_day=一週間の最低出勤日数
mw=男女の割合
age=多い年齢層
work=仕事の仕方
atm=職場の雰囲気
"""
def scrape():
    job_num : int = 0
    #総ページ数を取得
    page_number = open("./crawled_file/page_number.txt","r")
    page_num = page_number.read()
    page_number.close()
   
    #結果を保存するファイルに変数情報を入力
    info : str = "Num,企業名,勤務地,勤務形態,仕事内容,給与形態,金額,最低勤務日数(週1日~:1、週2.3~:2.5、週4~:4),交通費支給(有:1、無:0),年齢層(10代),年齢層(20代),年齢層(30代),年齢層(40代),年齢層(50代),男女比(5段階),仕事の仕方(5段階),職場の雰囲気(5段階)"
    newdir = "result_file2"
    if os.path.exists(newdir):
        print("exist.")
    else:
        os.mkdir(newdir)
    with open('./result_file2/result.csv','w',encoding="shift-jis") as file:
        file.write(info)
        file.write("\n")

    for i in range(1,int(page_num)+1): #全ページ
  
        baitoru_file = open("./crawled_file/baitoru_{}.html".format(i),"r")
        baitoru = baitoru_file.read()
        baitoru_file.close()
        bs = BeautifulSoup(baitoru, 'lxml')
        #各求人をページ毎にリストに保存
        job_list = bs.find_all("article", class_= "list-jobListDetail")
      
        for job in job_list: #ページ内の求人ごとに
            job_num = job_num + 1
            job_name : str = job.find("div",class_="pt02b").find("p").get_text().strip()
            job_tipe : str = job.find("div",class_="pt03").find_all("dl")[0].find("span").get_text().strip()
            job_point : str = job.find("div",class_="pt03").find_all("dl")[0].find("dd").get_text().strip()
            job_money : str = job.find("div",class_="pt03").find_all("dl")[1].find("em").get_text().strip()
            job_point = job_point.replace('\xa0','')
            job_point = job_point.replace('\t','')
            job_point = job_point.replace('\n','')
        
            #給料形態を取得する。このとき優先順位は時給、日給、月給、完全出来高制にする。
            job_money = job_money.replace(",","")
            money1 = re.search(r'時給(\d{3,5})円',job_money)
            if money1 is None:
                money2 = re.search(r'日給(\d{3,5})円',job_money)
                if money2 is None:
                    money3 = re.search(r'月給(.{0,5})円',job_money)
                    if money3 is None:
                        money4 = re.search(r'完全出来高制',job_money)
                        money_type : str = "完全出来高制"
                    else:
                        money_type : str = "月給"
                else:
                    money_type : str = "日給"
            else:
                money_type : str = "時給"
            
            job_traffic : str = job.find("ul",class_="ul02 nearest_station").find_all("li")[0].find("span").get_text().strip()
            #勤務条件をリストで取得
            job_condition : str = job.find("div",class_="pt04")
            trafic_money : int = 0
            job_day : int = 0
            if job_condition is None:
                traffic_money = 0
                job_day = 0
            else:
                job_condition = job_condition.find_all("em")
                flag : int = 0
                for job_con in job_condition:
                    job_con = job_con.get_text().strip()

                    if job_con == "交通費有":
                        trafic_money = 1
                    if job_con == "週1〜OK":
                        flag = 1
                        job_day = 1
                    elif flag!=1 and job_con == "週2・3〜OK":
                        flag = 1
                        job_day = 2.5
                    elif flag != 1 and job_con == "週4〜OK":
                        job_day = 4
            #最低賃金
            if money_type == "時給":
                money = money1.group(1)
            elif money_type == "日給":
                money = money2.group(1)
            elif money_type == "月給":
                money = money3.group(1)
            else:
                money = "完全出来高制"

            #新規求人の場合年齢層、男女の割合、仕事の仕方、職場の様子の項目がないため
            #ない場合はすべての項目を0にする
            four_mark : str = job.find("div",class_="pt05")
            if four_mark is None:
                age_mark : str = ",0,0,0,0,0"
                mw_mark : int = 0
                work_mark : int = 0
                atm_mark : int = 0
            #ちゃんと項目がある場合は
            else:
                #年齢層
                age_mark : str = ""
                age_li = job.find("dl",class_="dl01")
                if age_li is None:
                    age_mark : str = ",0,0,0,0,0"
                else:
                    age_li = age_li.find("ul",class_="ul01").find_all("li")
                    for age in age_li:
                        age = str(age)
                        mark = re.search("on",age)
                        if mark == None:
                            age_mark = age_mark + ",0"
                        else:
                            age_mark = age_mark + ",1"
                #男女の割合
                mw_mark : int = 0
                mw_li = job.find("dl",class_="dl02")
                j = 0
                if mw_li is None:
                  mw_mark : int = 0
                else:
                  mw_li = mw_li.find("ul",class_="ul01").find_all("li")
                  for mw in mw_li:
                      j = j + 1
                      mw = str(mw)
                      mark = re.search("on",mw)
                      if mark == None:
                          mw_mark = mw_mark + j*0
                      else:
                          mw_mark = mw_mark + j*1

                #仕事の仕方(一人で～大勢で)
                work_mark : int = 0
                work_li = job.find("dl",class_="dl03")
                j = 0
                if work_li is None:
                    work_mark : int = 0
                else:
                    work_li = work_li.find("ul",class_="ul01").find_all("li")
                    for work in work_li:
                        j = j + 1
                        work = str(work)
                        mark = re.search("on",work)
                        if mark == None:
                            work_mark = work_mark + j*0
                        else:
                            work_mark = work_mark + j*1
                #職場の様子(静か～にぎやか)
                atm_mark : int = 0
                atm_li = job.find("dl",class_="dl04")
                j = 0
                if atm_li is None:
                    atm_mark : int = 0
                else:
                    atm_li = atm_li.find("ul",class_="ul01").find_all("li")
                    for atm in atm_li:
                        j = j + 1
                        atm = str(atm)
                        mark = re.search("on",atm)
                        if mark == None:
                            atm_mark = atm_mark + j*0
                        else:
                            atm_mark = atm_mark + j*1
       
            """
            各変数を保存する
            data1 = 企業名　勤務地　勤務形態　仕事内容
            data2 = 給与形態　金額　最低勤務日数(週1日~:1, 週2,3~:2.5, 週4~:4)　交通費支給(有:1, 無:0)
            data3 = 年齢層(5段階) 男女比(5段階) 仕事の仕方(5段階) 職場の雰囲気(5段階)
            """
            
            data1 : str =  "," + job_name.replace(',','') + "," + job_traffic + "," + job_tipe + "," + job_point
            data2 : str =  "," + money_type + "," +  str(money) + "," + str(job_day) + "," + str(trafic_money)
            data3 : str =  str(age_mark) +  "," + str(mw_mark) + "," + str(work_mark) + "," + str(atm_mark)
            data4 : str = str(job_num) + data1 + data2 + data3
            data4 = data4.replace('①','')
            data4 = data4.replace('②','')
            data4 = data4.replace('③','')
            data4 = data4.replace('[','(')
            data4 = data4.replace(']',')')
            data4 = data4.replace('～','~')
            
            #データ保存
            print("{}ok".format(job_num))
            with open('./result_file2/result.csv', 'a' ,encoding="shift-jis") as file:
                file.write(data4)
                file.write("\n")
            
if __name__ == "__main__":
    scrape()
