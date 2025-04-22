import requests
from bs4 import BeautifulSoup
import csv 

date = input("Enter the date (in YYYY-MM-DD format): ")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(page) :

    src= page.content
    soup= BeautifulSoup(src, 'lxml')
    matches_details = []
    championships= soup.find_all('div', {'class': 'matchCard'})
    #print(championships)
    def get_match_info(championships):

       championship_title =championships.contents[1].find('h2').text.strip()
       print(championship_title)
       all_matches= championships.contents[3].find_all('div', {'class': 'item finish liItem'}) 
       number_of_matches=len(all_matches)
       print( number_of_matches)

       for i in range (number_of_matches):
           # get teams names 
           team_A = all_matches[i].find('div' , {'class' : 'teamA'}).text.strip()
           team_B = all_matches[i].find('div' , {'class' : 'teamB'}).text.strip()
           #get score 
           match_result=all_matches[i].find('div' , {'class' : 'MResult'}).find_all('span',{'class':'score'})
           score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

           #get time
           match_time = all_matches[i].find('div' , {'class' : 'MResult'}).find('span',{'class':'time'}).text.strip()

           #add match info to matches details
           matches_details.append({"نوع البطولة": championship_title , "الفريق الاول": team_A, "الفريق الثاني": team_B, "ميعاد المباراة": match_time , "النتيجة" : score})

    print("Number of the champions in the targeted content:", len(championships))

    for i in range (len(championships)) :
        get_match_info(championships[i])
    
    
    import pandas as pd

     # المسار الكامل للملف
    output_file = "documents/yallacorafile/matches_details.xlsx"

    df = pd.DataFrame(matches_details)

    # حفظ البيانات في ملف Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
     df.to_excel(writer, index=False)

     print("Excel File Created Successfully ✅")

    
    # keys = matches_details[0].keys() # matches_details : is a list of dectionaries and 0 is the first dictionary, so i retreived the keys of the first dictionary
    # with open ('documents/yallacorafile/matches_details.csv' , "w") as output_file :
    #    dict_writer =  csv.DictWriter(output_file, keys) #dict_writer is an object from DictWriter
    #    dict_writer.writeheader() #writeheader() : it writerow of matches_details بتاخد الكيس الي ادتهاله وبتكتبها كهيدر بتملي بيها اول صف  
    #    dict_writer.writerows(matches_details)
    #    print("File Created Successfully")

main(page)

 
