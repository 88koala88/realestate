import pandas as pd
import requests
import os
from bs4 import BeautifulSoup as bs
from datetime import datetime
from time import sleep

os.chdir("/home/ubuntu/realestate")
print(os.getcwd())


regal_code = pd.read_csv('data/regal_code.csv')

regal_code_seoul = regal_code[regal_code['시도명'] == '서울특별시']
regal_code_seoul = regal_code_seoul.reset_index(drop = True)
regal_code_list = regal_code_seoul['법정동시군구코드'].unique()
regal_code_seoul['시군구명'].unique()

# 년도
years = ['2020', '2021', '2022']

# 월
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# api 요청 변수 생성
years_month_list = []

for year in years :
    for month in months :
        year_month = str(year) + str(month)
        years_month_list.append(year_month)

regal_code_list
years_month_list

api_key = 'gdCwHED9I7qCHpJ2Umgc5tRA7zwN%2Fjj0sirO0Tz%2BahYoxq5vAGa0aO83isENeZvplygxLnlwI9%2Fk0wkfMyfCWw%3D%3D'
#LAWD_CD_VAL = '11110'
#DEAL_YMD_VAL = '202001'


# url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent?'
# params = 'serviceKey=' + api_key + '&' + \
#  'LAWD_CD=' + LAWD_CD_VAL + '&' + \
#  'DEAL_YMD=' + DEAL_YMD_VAL



# # requests, BeautifulSoup 라이브러리를 사용한 데이터 수집
# res = requests.get(url + params)
# soup = bs(res.text, 'xml')
# items = soup.find_all('item')


column_nm = [
 '거래금액',
 '거래유형',
 '건축년도',
 '년',
 '법정동',
 '아파트',
 '월',
 '일',
 '전용면적',
 '중개사소재지',
 '지번',
 '지역코드',
 '층',
 '해제사유발생일',
 '해제여부'
 ]


# total= pd.DataFrame()

# # 수집된 데이터를 Pandas 데이터 프레임 형식으로 변환
# for k in range(len(items)):
#     df_raw = []
#     for j in column_nm:
#         # print(LAWD_CD_list[i],k,j) # 에러 파악 여부
#         try:
#             items_data = items[k].find(j).text
#             df_raw.append(items_data)
#         except:
#             items_data = None
#             df_raw.append(items_data)

#     df = pd.DataFrame(df_raw).T
#     df.columns = column_nm
#     total = pd.concat([total, df])


file_nm = 'AptTrade'

if not os.path.exists(f'{file_nm}'):        # apt_rent가 존재하지 않을 경우 
    os.makedirs(f'{file_nm}')                # apt_rent 디렉토리 생성
    

for regal_code_val in regal_code_list:  # 법정동 코드
    for year_month_val in years_month_list: # 년월
        print(f'{regal_code_val}_{year_month_val}')
       
        url = f'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvc{file_nm}?'
        params = 'serviceKey=' + api_key + '&' + 'LAWD_CD=' + str(regal_code_val) + '&' + 'DEAL_YMD=' + year_month_val

        try:
            
            # requests, BeautifulSoup 라이브러리를 사용한 데이터 수집
            res = requests.get(url + params)
            soup = bs(res.text, 'xml')
            items = soup.find_all('item')
            
            print('data created')
            total = pd.DataFrame()

            # 수집된 데이터를 Pandas 데이터 프레임 형식으로 변환
            for k in range(len(items)):
                df_raw = []
                for j in column_nm:
                    # print(LAWD_CD_list[i],k,j) # 에러 파악 여부
                    try:
                        items_data = items[k].find(j).text
                        df_raw.append(items_data)
                    except:
                        items_data = None
                        df_raw.append(items_data)

                df = pd.DataFrame(df_raw).T
                df.columns = column_nm
                total = pd.concat([total, df])
    

            sleep(0.7)
            

            total.to_csv(f'{file_nm}/{regal_code_val}_{year_month_val}.csv',index = False)

            
            # log
            now = datetime.now()
            log_df = pd.DataFrame({
                'regal_code':regal_code_val,
                'year_month':year_month_val,
                'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'success'
                            
            },index = [0])
            
            if not os.path.exists(f'log_{file_nm}.csv'):
                log_df.to_csv(f'log_{file_nm}.csv', index = False, mode = 'w')
            else:
                log_df.to_csv(f'log_{file_nm}.csv', index = False, mode = 'a', header = False)    
            print('success')
            
         
        except:
            
            # log
            now = datetime.now()
            log_df = pd.DataFrame({
                'regal_code':regal_code_val,
                'year_month':year_month_val,
                'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'failed'
                            
            },index = [0])
            
            if not os.path.exists(f'log_{file_nm}.csv'):
                log_df.to_csv(f'log_{file_nm}.csv', index = False, mode = 'w')
            else:
                log_df.to_csv(f'log_{file_nm}.csv', index = False, mode = 'a', header = False)    

            print('failed')
