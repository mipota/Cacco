import requests
from bs4 import BeautifulSoup
import re
import csv
import os
def quest():

  csv_file = open("./result_file/result.csv", "r" , encoding="shift-jis", errors="", newline="" )
  #リスト形式
  csv_b = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
  """
   仕事内容について簡単化する
  - ティッシュ配り：サンプリング・ティッシュ配り・チラシ配り/ビラ配り、イベントスタッフ、アンケートモニター
  - ナイトワーク：フロアレディ・カウンターレディ(ナイトワーク系)、ガールズバー・キャバクラ・スナックその他(ナイトワーク系)、コスチューム系その他(ナイトワーク系)
  - データ入力：データ入力、タイピング(PC・パソコン・インターネット)、一般事務職、受付
  - 飲食：ホールスタッフ(配膳)、キッチンスタッフ
  - 接客・販売：レジ打ち
  - パチンコ：パチンコ・スロット(ホール)、パチンコ・スロット(カウンター)、案内(インフォメーション/レセプション)・フロント
  - プログラマー：システムエンジニア(SE)、プログラマー(PG)、インフラエンジニア/ネットワークエンジニア・運用
  - アパレル：アクセサリー・ジュエリー販売、アパレル(ファッション・服)、イベントスタッフ
  - 警備スタッフ：警備員、イベントスタッフ、サービスその他
  - 力仕事：軽作業・物流その他、資材搬入・荷揚げ、リフォーム・内装、品出し(ピッキング)、仕分け・シール貼り、倉庫管理・入出荷
  - ドライバー：配達・配送・宅配便、ドライバー・運転手、移転・引越し
  - 企画：企画営業、イベントスタッフ、企画・マーケティング
  - その他
  """
  
  info : str = "Num,企業名,勤務地,勤務形態,仕事内容,給与形態,金額,最低勤務日数(週1日~:1、週2.3~:2.5、週4~:4),交通費支給(有:1、無:0),年齢層(10代),年齢層(20代),年齢層(30代),年齢層(40代),年齢層(50代),男女比(5段階),仕事の仕方(5段階),職場の雰囲気(5段階)"
  with open('./result_file/rename.csv','w',encoding="shift-jis") as file:
    file.write(info)
    file.write("\n")
    file.close()
  #ヘッダを飛ばす
  next(csv_b)
  for data in csv_b:
    tag : str = re.search(r'ティッシュ配り',data[4])
    if tag is None:
      tag = re.search(r'ナイトワーク',data[4])
      if tag is None:
        tag = re.search(r'データ入力',data[4])
        if tag is None:
          tag = re.search(r'(ホールスタッフ)|(キッチンスタッフ)',data[4])
          if tag is None:
            tag = re.search(r'レジ打ち',data[4])
            if tag is None:
              tag = re.search(r'パチンコ',data[4])
              if tag is None:
                tag = re.search(r'(SE)|(PG)|(システムエンジニア)',data[4])
                if tag is None:
                  tag = re.search(r'アパレル',data[4])
                  if tag is None:
                    tag = re.search(r'警備',data[4])
                    if tag is None:
                      tag = re.search(r'(配達)|(ドライバー)|(運転)|(引っ越し)',data[4])
                      if tag is None:
                        tag = re.search(r'(軽作業)|(物流)|(仕分け)|(倉庫)',data[4])
                        if tag is None:
                          tag = re.search(r'(企画)|(マーケティング)',data[4])
                          if tag is None:
                            new_name : str = "その他"
                          else:
                            new_name : str = "企画"
                        else:
                          new_name : str = "力仕事"
                      else:
                        new_name : str = "ドライバー"
                    else:
                      new_name : str = "警備スタッフ"
                  else:
                    new_name : str = "アパレル"
                else:
                  new_name : str = "プログラマー"
              else:
                new_name : str = "パチンコ"
            else:
              new_name : str = "接客・販売"
          else:
            new_name : str = "飲食"
        else:
          new_name : str = "データ入力"
      else:
        new_name : str = "ナイトワーク"
    else:
      new_name : str = "ティッシュ配り"

    data[4] = new_name
    all_data : str = data[0]
    for i in range(1,17):
      all_data : str = all_data + "," + data[i] 
    with open('./result_file/rename.csv', 'a' ,encoding="shift-jis") as file:
      file.write(all_data)
      file.write("\n")
      
if __name__ == "__main__":
    quest()
