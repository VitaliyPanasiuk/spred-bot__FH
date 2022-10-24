from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.db import db_update

import gspread

import datetime
import asyncio
import json

class GoogleSheets:
    def __init__(self, filename, google_sheet_name):
        service_account = gspread.service_account(filename)
        self.sheet = service_account.open(google_sheet_name)


config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
bot2 = Bot(token=config.tg_bot.token2, parse_mode='HTML')


async def auf_status(user_id):
    base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
    cur = base.cursor() 
    cur.execute("SELECT * FROM users WHERE telegram_id = %s", (str(user_id),))
    user = cur.fetchall()
    answer = False
    if user:
        answer = True
    return answer

def get_settings_directions(user_id,spread_direction):
    base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
    cur = base.cursor() 
    cur.execute('''SELECT user_directions_exchanges.exchange_chosen, ub.bank_chosen, us.cryptocurrency_chosen, uo.operation_options_chosen, uf.fiat_currency_chosen
                            FROM user_directions_exchanges
                                LEFT JOIN user_directions_banks ub ON ub.user_id  = user_directions_exchanges.user_id and ub.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN user_directions_cryptocurrency us on us.user_id = user_directions_exchanges.user_id and us.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN user_directions_fiat_currency uf on uf.user_id = user_directions_exchanges.user_id and uf.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN user_directions_operation_options uo on uo.user_id = user_directions_exchanges.user_id and uo.spread_direction = user_directions_exchanges.spread_direction
                                LEFT JOIN users ON users.id = user_directions_exchanges.user_id
                                LEFT JOIN spread_directions ON spread_directions.id = user_directions_exchanges.spread_direction
                        WHERE users.telegram_id = %s and spread_directions.name = %s''', (str(user_id), spread_direction))
    directions = cur.fetchone()
    print ('settings')
    print(directions)
    return directions

async def parse_binance1(result,settings,min_spread):
    flagtext2 = False
    message = ''
    
    # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
    # worksheet = service.sheet.worksheet(sheet)
    # result = worksheet.get(rang)
    
    for i in result:
        if i == []:
            result.remove(i)
    for row in range(len(result[0])):
        if row != 0:
            flagbank = True
            bank = result[0][row].replace(' ','').split('→')
            for i in bank:
                if i not in settings[1]:
                    flagbank = False
            if flagbank:
                for line in range(len(result)):
                    if line != 0:
                        try:
                            num = float(result[line][row].replace(',','.'))
                            # if type(num) == int or type(num) == float:
                            if result[line][row]:
                                num = num/1000
                                if result[line][0] in settings[2] and num > min_spread[0]:
                                    if not flagtext2:
                                        message += f'\n{result[0][0]}\n'
                                        flagtext2 = True
                                    message += f'{result[0][row]}  + {result[line][0]} + {str(round(float(num),2))} %\n'
                        except:
                            pass
    return message

async def parse_binance2(result,settings,min_spread):
    flagtext2 = False
    message = ''
    
    # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
    # worksheet = service.sheet.worksheet(sheet)
    # result = worksheet.get(rang)
    
    for i in result:
        if i == []:
            result.remove(i)
    
        
    for row in range(len(result[0])):
        if row != 0:
            flagcr = True
            flagbank = True
            cr = result[0][row].replace(' ','').split('→')
            for i in cr:
                if i not in settings[2]:
                    flagcr = False
            if flagcr:
                for line in range(len(result)):
                    if line != 0:
                        try:
                            num = float(result[line][row].replace(',','.'))
                            # if type(num) == int or type(num) == float:
                            num = num/1000
                            bank = result[line][0].replace(' ','').split('→')
                            for b in bank:
                                if b not in settings[1]:
                                    flagbank = False
                            if flagbank and num > min_spread[0]:
                                if not flagtext2:
                                    message += f'\n{result[0][0]}\n'
                                    flagtext2 = True
                                message += f'{result[line][0]} + {result[0][row]}  +  {str(round(float(num),2))} %\n'
                        except:
                            pass
                        
    return message

async def parse_binance3(result,settings,min_spread):
    flagtext2 = False
    message = ''
    
    # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
    # worksheet = service.sheet.worksheet(sheet)
    # result = worksheet.get(rang)
    
    for i in result:
        if i == []:
            result.remove(i)
    
        
    for row in range(len(result[0])):
        if row != 0:
            flagcr = True
            flagbank = True
            cr = result[0][row].replace(' ','').split('→')
            for i in cr:
                if i not in settings[4]:
                    flagcr = False
            if flagcr:
                for line in range(len(result)):
                    if line != 0:
                        try:
                            num = float(result[line][row].replace(',','.'))
                            # if type(num) == int or type(num) == float:
                            num = num.replace(',','.')/1000
                            # bank = result[line][0].replace(' ','').split('→')
                            # for b in bank:
                            if result[line][0] not in settings[2]:
                                flagbank = False
                            if flagbank and num > min_spread[0]:
                                if not flagtext2:
                                    message += f'\n{result[0][0]}\n'
                                    flagtext2 = True
                                message += f'{result[line][0]} + {result[0][row]} +  {str(round(float(num),2))} %\n'
                        except:
                            pass
    return message
    
async def mailing():
    while True:
        print('start mailing')
        base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
        cur = base.cursor() 
        cur.execute("SELECT * FROM users WHERE spreads_on = true")
        users = cur.fetchall()
        
        service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
        service2=GoogleSheets(filename='cred2.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
        all_sheets = service.sheet.worksheets()
    
        sh = all_sheets[0]
        worksheet = service.sheet.worksheet(sh.title)
        
        result = worksheet.get('A11:H13')
        result2 = worksheet.get('A15:G41')
        result3 = worksheet.get('A47:F49')
        result4 = worksheet.get('A51:E69')
        result5 = worksheet.get('A75:F77')
        result6 = worksheet.get('A79:E97')
        
        sh = all_sheets[1]
        worksheet2 = service.sheet.worksheet(sh.title)
        result7 = worksheet2.get('A7:E9')
        result8 = worksheet2.get('A11:E13')
        result9 = worksheet2.get('A15:E17')
        result10 = worksheet2.get('A19:E21')
        result11 = worksheet2.get('A23:E25')
        result12 = worksheet2.get('A27:E29')
        result20 = worksheet2.get('G7:K9')
        result21 = worksheet2.get('G11:K13')
        result22 = worksheet2.get('G15:K17')
        result23 = worksheet2.get('G19:K21')
        result24 = worksheet2.get('G23:K25')
        result25 = worksheet2.get('G27:K29')
        
        sh = all_sheets[2]
        worksheet3 = service.sheet.worksheet(sh.title)
        result13 = worksheet3.get('A10:E14')
        result14 = worksheet3.get('G10:I14')
        
        sh = all_sheets[3]
        worksheet4 = service.sheet.worksheet(sh.title)
        arrB1 = []
        arrB2 = []
        ranges = ['A69:J77','A58:K66','A80:J88','A91:J99','A102:J110','A113:J121','A124:J132','A135:J143','A146:J154','A157:J165','A168:J176']
        ranges2 = ['A192:F292','A295:F395','A398:F498','A501:F601','A604:F704','A707:F807']
        for i in ranges:
            res = worksheet4.get(i)
            arrB1.append(res)
        for i in ranges2:
            res = worksheet4.get(i)
            arrB2.append(res)
            
        sh = all_sheets[7]
        worksheet5 = service2.sheet.worksheet(sh.title)
        arrOKX1 = []
        arrOKX2 = []
        ranges = ['A22:F26','A28:E32','A34:E38','A40:E44','A46:E50','A52:E55']
        ranges2 = ['A60:C84','E60:G84','I60:K84']
        for i in ranges:
            res = worksheet5.get(i)
            arrB1.append(res)
        for i in ranges2:
            res = worksheet5.get(i)
            arrB2.append(res)
            
        sh = all_sheets[10]
        worksheet6 = service2.sheet.worksheet(sh.title)
        arrByBit1 = []
        arrByBit2 = []
        ranges = ['A25:F29','A31:E35','A37:E41','A43:E47','A49:E53','A55:E59']
        ranges2 = ['A63:C87','E63:G87','I63:K87']
        for i in ranges:
            res = worksheet6.get(i)
            arrByBit1.append(res)
        for i in ranges2:
            res = worksheet6.get(i)
            arrByBit2.append(res)
            
        sh = all_sheets[11]
        worksheet7 = service2.sheet.worksheet(sh.title)
        arrWise1 = []
        arrWise2 = []
        ranges = ['A20:F25']
        ranges2 = ['A30:E35','A37:E42','A44:E49','A50:E56']
        for i in ranges:
            res = worksheet7.get(i)
            arrWise1.append(res)
        for i in ranges2:
            res = worksheet7.get(i)
            arrWise2.append(res)
            
        sh = all_sheets[13]
        worksheet8 = service2.sheet.worksheet(sh.title)
        arrLocalBitcoins = []
        ranges = ['A19:C29']
        for i in ranges:
            res = worksheet8.get(i)
            arrLocalBitcoins.append(res)
        
        for user in users:
            try:
                cur.execute(''' SELECT spread_directions.name
                                    FROM is_direction_on_for_user
                                    LEFT JOIN spread_directions ON spread_directions.id = is_direction_on_for_user.spread_direction
                                    LEFT JOIN users ON users.id = is_direction_on_for_user.user_id
                                        WHERE users.telegram_id = %s and is_direction_on_for_user.is_on = true''', (str(user[1]),))
                spread_directions = cur.fetchall()
                for spread_direction in spread_directions:
                    cur.execute(''' SELECT user_directions_exchanges.exchange_chosen, ub.bank_chosen, us.cryptocurrency_chosen, uo.operation_options_chosen, uf.fiat_currency_chosen
                                        FROM user_directions_exchanges
                                            LEFT JOIN user_directions_banks ub ON ub.user_id  = user_directions_exchanges.user_id and ub.spread_direction = user_directions_exchanges.spread_direction
                                            LEFT JOIN user_directions_cryptocurrency us on us.user_id = user_directions_exchanges.user_id and us.spread_direction = user_directions_exchanges.spread_direction
                                            LEFT JOIN user_directions_fiat_currency uf on uf.user_id = user_directions_exchanges.user_id and uf.spread_direction = user_directions_exchanges.spread_direction
                                            LEFT JOIN user_directions_operation_options uo on uo.user_id = user_directions_exchanges.user_id and uo.spread_direction = user_directions_exchanges.spread_direction
                                            LEFT JOIN users ON users.id = user_directions_exchanges.user_id
                                            LEFT JOIN spread_directions ON spread_directions.id = user_directions_exchanges.spread_direction
                                    WHERE users.telegram_id = %s and spread_directions.name = %s''', (str(user[1]), spread_direction))
                    settings = cur.fetchall()
                    settings = settings[0]
                    
                    cur.execute(''' SELECT ms.spread_value
                                        FROM users
                                            LEFT JOIN is_direction_on_for_user isd on isd.user_id = users.id
                                            LEFT JOIN minimal_spread ms ON ms.user_id  = users.id and ms.spread_direction = isd.spread_direction
                                    WHERE telegram_id = %s ORDER BY ms.spread_direction''',(str(user[1]),))
                    min_spread = cur.fetchall()
                    
                    if spread_direction[0] == 'Найпростіші (Найліквідніші) зв’язки':
                        message = ''
                        if settings[0] and 'Binance' in settings[0]:
                            flagtext2 = False
                            
                            # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                            # all_sheets = service.sheet.worksheets()
                            # sh = all_sheets[0]

                            # worksheet = service.sheet.worksheet(sh.title)
                            # result = worksheet.get('A11:H13')
                            
                            for i in result:
                                if i == []:
                                    result.remove(i)
                            
                            for line in range(len(result)):
                                if line < len(result):
                                    for a in range(len(result[line])):
                                        if a != 0:
                                            bank = result[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                            if flag == True:
                                                try:
                                                    num = result[line+1][a].replace('%','').replace(',','.')
                                                    if float(num) > min_spread[0][0]:
                                                        print(True)
                                                        if flag:
                                                            if not flagtext2:
                                                                message += 'Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result[0][0]}\n'
                                                                flagtext = True
                                                            
                                                            message += f'{result[line][a]} {result[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass
                                                        
                            # result = worksheet.get('A15:G41') res 2
                            
                            for i in result2:
                                if i == []:
                                    result2.remove(i)

                            
                            for line in range(len(result2)):
                                if line < len(result2):
                                    for a in range(len(result2[line])):
                                        if a != 0:
                                            bank = result2[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result2[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if  float(num) > min_spread[0][0]:
                                                        print(True)
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nBinance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result2[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result2[line][a]} {result2[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass
                        if settings[0] and 'ByBit' in settings[0]:
                            flagtext2 = False
                            # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                            # all_sheets = service.sheet.worksheets()
                            # sh = all_sheets[0]

                            # worksheet = service.sheet.worksheet(sh.title)
                            # result = worksheet.get('A47:F49') res 3
                            
                            for i in result3:
                                if i == []:
                                    result3.remove(i)
                            
                            for line in range(len(result3)):
                                if line < len(result3):
                                    for a in range(len(result3[line])):
                                        if a != 0:
                                            bank = result3[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                            if flag == True:
                                                try:
                                                    num = result3[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if  float(num) > min_spread[0][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                    message += '\nByBit\n'
                                                                    flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result3[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result3[line][a]} {result3[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass
                            # result = worksheet.get('A15:G41') res 4
                            
                            for i in result4:
                                if i == []:
                                    result4.remove(i)
                            
                            for line in range(len(result4)):
                                if line < len(result4):
                                    if line < len(result4):
                                        for a in range(len(result4[line])):
                                            if a != 0:
                                                bank = result4[line][a].replace(' ','').split('→')
                                                flag = True
                                                flagtext = False
                                                for i in bank:
                                                    if i not in settings[1]:
                                                        print(i)
                                                        flag = False
                                                print(bank,settings[1],flag)
                                                if flag == True:
                                                    try:
                                                        num = result4[line+1][a].replace('%','').replace(',','.')
                                                        
                                                        if float(num) > min_spread[0][0]:
                                                            
                                                            if flag:
                                                                if not flagtext2:
                                                                    message += '\nByBit\n'
                                                                    flagtext2 = True
                                                                if not flagtext:
                                                                    message += f'{result4[0][0]}\n'
                                                                    flagtext = True
                                                                message += f'{result4[line][a]} {result4[line+1][0]} +{str(round(float(num),2))} %\n'
                                                    except:
                                                        pass
                                                            
                        if settings[0] and settings[0] and  'OKX' in settings[0]:
                            flagtext2 = False
                            # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                            # all_sheets = service.sheet.worksheets()
                            # sh = all_sheets[0]

                            # worksheet = service.sheet.worksheet(sh.title)
                            # result = worksheet.get('A47:F49') res 5
                            
                            for i in result5:
                                if i == []:
                                    result5.remove(i)
                            
                            for line in range(len(result5)):
                                if line < len(result5):
                                    if line < len(result5):
                                        for a in range(len(result5[line])):
                                            if a != 0:
                                                bank = result5[line][a].replace(' ','').split('→')
                                                flag = True
                                                flagtext = False
                                                for i in bank:
                                                    if i not in settings[1]:
                                                        flag = False
                                                
                                                if flag == True:
                                                    try:
                                                        num = result5[line+1][a].replace('%','').replace(',','.')
                                                        
                                                        if  float(num) > min_spread[0][0]:
                                                            if flag:
                                                                if not flagtext2:
                                                                    message += '\nOKX\n'
                                                                    flagtext2 = True
                                                                if not flagtext:
                                                                    message += f'{result5[0][0]}\n'
                                                                    flagtext = True
                                                                
                                                                message += f'{result5[line][a]} {result5[line+1][0]} +{str(round(float(num),2))} %\n'
                                                    except:
                                                        pass        
                            # result = worksheet.get('A15:G41') 6
                            
                            for i in result6:
                                if i == []:
                                    result6.remove(i)
                            
                            for line in range(len(result6)):
                                if line < len(result6):
                                    if line < len(result6):
                                        for a in range(len(result6[line])):
                                            if a != 0:
                                                bank = result6[line][a].replace(' ','').split('→')
                                                flag = True
                                                flagtext = False
                                                for i in bank:
                                                    if i not in settings[1]:
                                                        flag = False
                                                if flag == True:
                                                    try:
                                                        num = result6[line+1][a].replace('%','').replace(',','.')
                                                        if float(num) > min_spread[0][0]:
                                                            if flag:
                                                                if not flagtext2:
                                                                    message += '\nOKX\n'
                                                                    flagtext2 = True
                                                                if not flagtext:
                                                                    message += f'{result6[0][0]}\n'
                                                                    flagtext = True
                                                                message += f'{result6[line][a]} {result6[line+1][0]} +{str(round(float(num),2))} %\n'
                                                    except:
                                                        pass
                        if message:
                            print('send simple message')
                            await bot2.send_message(user[1],message)
                    
                    if spread_direction[0] == 'Міжбіржові':
                        message = ''
                        if settings[0] and settings[0] and 'Binance' in settings[0] and 'ByBit' in settings[0]:
                            flagtext2 = False
                            
                            
                            # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                            # all_sheets = service.sheet.worksheets()
                            # sh = all_sheets[1]

                            # worksheet = service.sheet.worksheet(sh.title)
                            # result = worksheet.get('A7:E9') res 7
                            
                            for i in result7:
                                if i == []:
                                    result7.remove(i)
                            
                                
                            for line in range(len(result7)):
                                if line < len(result7):
                                    for a in range(len(result7[line])):
                                        if a != 0:
                                            bank = result7[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                            if flag == True:
                                                try:
                                                    num = result7[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += 'Купуємо на ByBit продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result7[0][0]}\n'
                                                                flagtext = True
                                                            
                                                            message += f'{result7[line][a]} {result7[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass                
                            # result = worksheet.get('A11:E13') res 8
                            
                            for i in result8:
                                if i == []:
                                    result8.remove(i)

                            
                            for line in range(len(result8)):
                                if line < len(result8):
                                    for a in range(len(result8[line])):
                                        if a != 0:
                                            bank = result8[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result8[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result8[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result8[line][a]} {result8[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('A15:E17') res 9
                            
                            for i in result9:
                                if i == []:
                                    result9.remove(i)

                            
                            for line in range(len(result9)):
                                if line < len(result9):
                                    for a in range(len(result9[line])):
                                        if a != 0:
                                            bank = result9[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result9[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result9[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result9[line][a]} {result9[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('A19:E21') res 10
                            
                            for i in result10:
                                if i == []:
                                    result10.remove(i)

                            
                            for line in range(len(result10)):
                                if line < len(result10):
                                    for a in range(len(result10[line])):
                                        if a != 0:
                                            bank = result10[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result10[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result10[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result10[line][a]} {result10[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('A23:E25') res 11
                            
                            for i in result11:
                                if i == []:
                                    result11.remove(i)

                            
                            for line in range(len(result11)):
                                if line < len(result11):
                                    for a in range(len(result11[line])):
                                        if a != 0:
                                            bank = result11[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result11[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result11[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result11[line][a]} {result11[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('A27:E29') res 12
                            
                            for i in result12:
                                if i == []:
                                    result12.remove(i)

                            
                            for line in range(len(result12)):
                                if line < len(result12):
                                    for a in range(len(result12[line])):
                                        if a != 0:
                                            bank = result12[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result12[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result12[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result12[line][a]} {result12[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                        if settings[0] and 'Binance' in settings[0] and 'OKX' in settings[0]:
                            flagtext2 = False
                            
                            
                            # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                            # all_sheets = service.sheet.worksheets()
                            # sh = all_sheets[1]

                            # worksheet = service.sheet.worksheet(sh.title)
                            # result = worksheet.get('G7:K9') res 20
                            
                            for i in result20:
                                if i == []:
                                    result20.remove(i)
                            
                                
                            for line in range(len(result20)):
                                if line < len(result20):
                                    for a in range(len(result20[line])):
                                        if a != 0:
                                            bank = result20[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                            print(bank,settings[1],flag)
                                            if flag == True:
                                                try:
                                                    num = result20[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        if flag:
                                                            if not flagtext2:
                                                                message += 'Купуємо на OKX продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result20[0][0]}\n'
                                                                flagtext = True
                                                            
                                                            message += f'{result20[line][a]} {result20[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass 
                            # result = worksheet.get('G11:K13') res 21
                            
                            for i in result21:
                                if i == []:
                                    result21.remove(i)

                            
                            for line in range(len(result21)):
                                if line < len(result21):
                                    for a in range(len(result21[line])):
                                        if a != 0:
                                            bank = result21[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result21[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if  float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на OKX продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result21[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result21[line][a]} {result21[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('G15:K17') res 22
                            
                            for i in result22:
                                if i == []:
                                    result22.remove(i)

                            
                            for line in range(len(result22)):
                                if line < len(result22):
                                    for a in range(len(result22[line])):
                                        if a != 0:
                                            bank = result22[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result22[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на OKX продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result22[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result22[line][a]} {result22[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('G19:K21') res 23
                            
                            for i in result23:
                                if i == []:
                                    result23.remove(i)

                            
                            for line in range(len(result23)):
                                if line < len(result23):
                                    for a in range(len(result23[line])):
                                        if a != 0:
                                            bank = result23[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result23[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на OKX продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result23[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result23[line][a]} {result23[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('G23:K25') res 24
                            
                            for i in result24:
                                if i == []:
                                    result24.remove(i)

                            
                            for line in range(len(result24)):
                                if line < len(result24):
                                    for a in range(len(result24[line])):
                                        if a != 0:
                                            bank = result24[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result24[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на OKX продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result24[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result24[line][a]} {result24[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass         
                            # result = worksheet.get('G27:K29') res 25
                            
                            for i in result25:
                                if i == []:
                                    result25.remove(i)

                            
                            for line in range(len(result25)):
                                if line < len(result25):
                                    for a in range(len(result25[line])):
                                        if a != 0:
                                            bank = result25[line][a].replace(' ','').split('→')
                                            flag = True
                                            flagtext = False
                                            for i in bank:
                                                if i not in settings[1]:
                                                    flag = False
                                                    
                                            if flag == True:
                                                try:
                                                    num = result25[line+1][a].replace('%','').replace(',','.')
                                                    
                                                    if float(num) > min_spread[1][0]:
                                                        
                                                        if flag:
                                                            if not flagtext2:
                                                                message += '\nКупуємо на OKX продаємо на Binance\n'
                                                                flagtext2 = True
                                                            if not flagtext:
                                                                message += f'{result25[0][0]}\n'
                                                                flagtext = True
                                                            message += f'{result25[line][a]} {result25[line+1][0]} +{str(round(float(num),2))} %\n'
                                                except:
                                                    pass 
                        if message:
                            print('send intersex message')
                            
                            await bot2.send_message(user[1],message)
                    
                    if spread_direction[0] == 'Готівка':
                        message = ''
                        if settings[0] and 'Binance' in settings[0]:
                                flagtext2 = False
                                
                                
                                # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                                # all_sheets = service.sheet.worksheets()
                                # sh = all_sheets[2]

                                # worksheet = service.sheet.worksheet(sh.title)
                                # result = worksheet.get('A10:E14') res 13
                                
                                for i in result13:
                                    if i == []:
                                        result13.remove(i)
                                
                                    
                                for row in range(len(result13[0])):
                                    cr = result13[0][row].split(' ')
                                    if cr[1] in settings[2]:
                                        for line in range(len(result13)):
                                            if line != 0:
                                                try:
                                                # if type(result13[line][row]) == int or type(result13[line][row]) == float:
                                                    num = float(result13[line][row])/1000
                                                    if result13[line][0] in settings[1] and num > min_spread[2][0]:
                                                        if not flagtext2:
                                                            message += '\nBinance профіт\n'
                                                            flagtext2 = True
                                                        message += f'{result13[line][0]}+ {result13[0][row]}  + {round(float(num),2)} %\n'
                                                except: 
                                                    pass
                        if settings[0] and 'ByBit' in settings[0]:
                                flagtext2 = False
                                
                                
                                # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                                # all_sheets = service.sheet.worksheets()
                                # sh = all_sheets[2]

                                # worksheet = service.sheet.worksheet(sh.title)
                                # result = worksheet.get('G10:I14') res 14
                                
                                for i in result14:
                                    if i == []:
                                        result14.remove(i)
                                
                                    
                                for row in range(len(result14[0])):
                                    cr = result14[0][row].split(' ')
                                    if cr[1] in settings[2]:
                                        for line in range(len(result14)):
                                            if line != 0:
                                                try:
                                                    num = float(result14[line][row])/1000
                                                    if result14[line][0] in settings[1] and num > min_spread[2][0]:
                                                        if not flagtext2:
                                                            message += '\nByBit профіт\n'
                                                            flagtext2 = True
                                                        message += f'{result14[line][0]}+ {result14[0][row]}  + {str(round(float(num),2))} %\n'                        
                                                except: 
                                                    pass
                        if message:
                            print('send cash message')
                            
                            await bot2.send_message(user[1],message)
                    
                    if spread_direction[0] == 'Binance':
                        message = ''
                        # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        # all_sheets = service.sheet.worksheets()
                        # sh = all_sheets[3]
                        if 'Купуємо крипту, продаємо її' in settings[3]:
                            # ranges = ['A69:J77','A58:K66','A80:J88','A91:J99','A102:J110','A113:J121','A124:J132','A135:J143','A146:J154','A157:J165','A168:J176']
                            # for i in ranges:
                            #     mess = await parse_binance1(i,settings,min_spread[3])
                            #     message += mess
                            for i in arrB1:
                                mess = await parse_binance1(i,settings,min_spread[3])
                                message += mess
                        if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' in settings[3]:
                            # ranges = ['A192:F292','A295:F395','A398:F498','A501:F601','A604:F704','A707:F807']
                            # for i in ranges:
                            #     mess = await parse_binance2(i,settings,min_spread[3])
                            #     message += mess
                            for i in arrB2:
                                mess = await parse_binance1(i,settings,min_spread[3])
                                message += mess
                        if message:
                            if len(message) > 4096:
                                for x in range(0, len(message), 4096):
                                    await bot2.send_message(user[1], message[x:x+4096])
                            else:
                                await bot2.send_message(user[1], message)
                            
                    if spread_direction[0] == 'OKX':
                        message = ''
                        # service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        # all_sheets = service.sheet.worksheets()
                        # sh = all_sheets[7]
                        if 'Купуємо крипту, продаємо її' in settings[3]:
                            ranges = ['A22:F26','A28:E32','A34:E38','A40:E44','A46:E50','A52:E55']
                            for i in ranges:
                                mess = await parse_binance1(i,settings,min_spread[4])
                                message += mess
                        if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' in settings[3]:
                            ranges = ['A60:C84','E60:G84','I60:K84']
                            for i in ranges:
                                mess = await parse_binance2(i,settings,min_spread[4])
                                message += mess
                        if message:
                            if len(message) > 4096:
                                for x in range(0, len(message), 4096):
                                    await bot2.send_message(user[1], message[x:x+4096])
                            else:
                                await bot2.send_message(user[1], message)

                    if spread_direction[0] == 'ByBit':
                        message = ''
                        service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        all_sheets = service.sheet.worksheets()
                        sh = all_sheets[10]
                        if 'Купуємо крипту, продаємо її' in settings[3]:
                            ranges = ['A25:F29','A31:E35','A37:E41','A43:E47','A49:E53','A55:E59']
                            for i in ranges:
                                mess = await parse_binance1(i,settings,min_spread[5])
                                message += mess
                        if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' in settings[3]:
                            ranges = ['A63:C87','E63:G87','I63:K87']
                            for i in ranges:
                                mess = await parse_binance2(i,settings,min_spread[5])
                                message += mess
                        if message:
                            if len(message) > 4096:
                                for x in range(0, len(message), 4096):
                                    await bot2.send_message(user[1], message[x:x+4096])
                            else:
                                await bot2.send_message(user[1], message)
                            
                    if spread_direction[0] == 'Wise':
                        message = ''
                        service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        all_sheets = service.sheet.worksheets()
                        sh = all_sheets[11]
                        if 'Купуємо крипту та продаємо (одна платіжна система)' in settings[3]:
                            ranges = ['A20:F25']
                            for i in ranges:
                                mess = await parse_binance3(i,settings,min_spread[6])
                                message += mess
                        if 'Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система)' in settings[3]:
                            ranges = ['A30:E35','A37:E42','A44:E49','A50:E56']
                            for i in ranges:
                                mess = await parse_binance3(i,settings,min_spread[6])
                                message += mess
                        if message:
                            if len(message) > 4096:
                                for x in range(0, len(message), 4096):
                                    await bot2.send_message(user[1], message[x:x+4096])
                            else:
                                await bot2.send_message(user[1], message)

                    if spread_direction[0] == 'LocalBitcoins':
                        message = ''
                        service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        all_sheets = service.sheet.worksheets()
                        sh = all_sheets[13]
                        ranges = ['A19:C29']
                        for i in ranges:
                            mess = await parse_binance2(i,settings,min_spread[7])
                            message += mess
                        if message:
                            if len(message) > 4096:
                                for x in range(0, len(message), 4096):
                                    await bot2.send_message(user[1], message[x:x+4096])
                            else:
                                await bot2.send_message(user[1], message)

            except:
                print('none data')
            
        await asyncio.sleep(60)                                      

async def check_sub():
    while True:
        base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
        cur = base.cursor() 
        # cur.execute("SELECT * FROM users WHERE spreads_on = true")
        # users = cur.fetchone()
        cur.execute("SELECT * FROM user_subscriptions")
        users = cur.fetchall()
        for user in users:
            now = datetime.datetime.now()
            if now >= user[2]:
                cur.execute("DELETE FROM user_subscriptions WHERE id = %s",(user[0],))
                base.commit()
            
        
        await asyncio.sleep(300)
