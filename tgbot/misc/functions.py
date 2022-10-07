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

async def parse_binance1(rang,settings,min_spread,sheet):
    flagtext2 = False
    message = ''
    
    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
    worksheet = service.sheet.worksheet(sheet)
    result = worksheet.get(rang)
    
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
                        if result[line][row].isdigit():
                            num = result[line][row]/1000
                            if result[line][0] in settings[2] and num > min_spread[0]:
                                if not flagtext2:
                                    message += '\n{result[0][0]}\n'
                                    flagtext2 = True
                                message += f'{result[0][row]}  + {result[line][0]} + {num}%\n'
    return message

async def parse_binance2(rang,settings,min_spread,sheet):
    flagtext2 = False
    message = ''
    
    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
    worksheet = service.sheet.worksheet(sheet)
    result = worksheet.get(rang)
    
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
                        if result[line][row].isdigit():
                            num = result[line][row]/1000
                            bank = result[line][0].replace(' ','').split('→')
                            for b in bank:
                                if b not in settings[1]:
                                    flagbank = False
                            if flagbank and num > min_spread[0]:
                                if not flagtext2:
                                    message += '\n{result[0][0]}\n'
                                    flagtext2 = True
                                message += f'{result[line][0]} + {result[0][row]}  +  {num}%\n'
    return message

async def parse_binance3(rang,settings,min_spread,sheet):
    flagtext2 = False
    message = ''
    
    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
    worksheet = service.sheet.worksheet(sheet)
    result = worksheet.get(rang)
    
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
                        if result[line][row].isdigit():
                            num = result[line][row]/1000
                            # bank = result[line][0].replace(' ','').split('→')
                            # for b in bank:
                            if result[line][0] not in settings[2]:
                                flagbank = False
                            if flagbank and num > min_spread[0]:
                                if not flagtext2:
                                    message += '\n{result[0][0]}\n'
                                    flagtext2 = True
                                message += f'{result[line][0]} + {result[0][row]}  +  {num}%\n'
    return message
    
async def mailing():
    while True:
        base = psycopg2.connect(dbname=config.db.database, user=config.db.user, password=config.db.password,host=config.db.host)
        cur = base.cursor() 
        cur.execute("SELECT * FROM users WHERE spreads_on = true")
        users = cur.fetchall()
        
        for user in users:
            message = ''
            cur.execute(''' SELECT spread_directions.name
                            FROM is_direction_on_for_user
                            LEFT JOIN spread_directions ON spread_directions.id = is_direction_on_for_user.spread_direction
                            LEFT JOIN users ON users.id = is_direction_on_for_user.user_id
                            WHERE users.telegram_id = %s''', ('762342298',))
            spread_direction = cur.fetchone()
            
            cur.execute(''' SELECT user_directions_exchanges.exchange_chosen, ub.bank_chosen, us.cryptocurrency_chosen, uo.operation_options_chosen, uf.fiat_currency_chosen
                                FROM user_directions_exchanges
                                    LEFT JOIN user_directions_banks ub ON ub.user_id  = user_directions_exchanges.user_id and ub.spread_direction = user_directions_exchanges.spread_direction
                                    LEFT JOIN user_directions_cryptocurrency us on us.user_id = user_directions_exchanges.user_id and us.spread_direction = user_directions_exchanges.spread_direction
                                    LEFT JOIN user_directions_fiat_currency uf on uf.user_id = user_directions_exchanges.user_id and uf.spread_direction = user_directions_exchanges.spread_direction
                                    LEFT JOIN user_directions_operation_options uo on uo.user_id = user_directions_exchanges.user_id and uo.spread_direction = user_directions_exchanges.spread_direction
                                    LEFT JOIN users ON users.id = user_directions_exchanges.user_id
                                    LEFT JOIN spread_directions ON spread_directions.id = user_directions_exchanges.spread_direction
                            WHERE users.telegram_id = %s and spread_directions.name = %s''', (str(user[1]), spread_direction[0]))
            settings = cur.fetchall()
            settings = settings[0]
            
            cur.execute(''' SELECT ms.spread_value
                                FROM users
                                    LEFT JOIN minimal_spread ms ON ms.user_id  = users.id
                            WHERE telegram_id = %s''',(str(user[1]),))
            min_spread = cur.fetchone()
            
            if spread_direction[0] and spread_direction[0] == 'Найпростіші (Найліквідніші) зв’язки':
                if settings[0] and 'Binance' in settings[0]:
                    flagtext2 = False
                    
                    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                    all_sheets = service.sheet.worksheets()
                    sh = all_sheets[0]

                    worksheet = service.sheet.worksheet(sh.title)
                    result = worksheet.get('A11:H13')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += 'Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                    
                    result = worksheet.get('A15:G41')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                if settings[0] and 'ByBit' in settings[0]:
                    flagtext2 = False
                    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                    all_sheets = service.sheet.worksheets()
                    sh = all_sheets[0]

                    worksheet = service.sheet.worksheet(sh.title)
                    result = worksheet.get('A47:F49')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                        message += '\nByBit\n'
                                                        flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('A15:G41')
                    
                    for i in result:
                        if i == []:
                            result.remove(i)
                    
                    for line in range(len(result)):
                        if line < len(result):
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
                                            num = result[line+1][a].replace('%','').replace(',','.')
                                            
                                            if float(num) > 0.5:
                                                
                                                if flag:
                                                    if not flagtext2:
                                                        message += '\nByBit\n'
                                                        flagtext2 = True
                                                    if not flagtext:
                                                        message += f'{result[0][0]}\n'
                                                        flagtext = True
                                                    message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                    
                if settings[0] and settings[0] and  'OKX' in settings[0]:
                    flagtext2 = False
                    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                    all_sheets = service.sheet.worksheets()
                    sh = all_sheets[0]

                    worksheet = service.sheet.worksheet(sh.title)
                    result = worksheet.get('A47:F49')
                    
                    for i in result:
                        if i == []:
                            result.remove(i)
                    
                        
                    for line in range(len(result)):
                        if line < len(result):
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
                                            num = result[line+1][a].replace('%','').replace(',','.')
                                            
                                            if float(num) > 0.5:
                                                
                                                if flag:
                                                    if not flagtext2:
                                                        message += '\nOKX\n'
                                                        flagtext2 = True
                                                    if not flagtext:
                                                        message += f'{result[0][0]}\n'
                                                        flagtext = True
                                                    
                                                    message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                    
                    result = worksheet.get('A15:G41')
                    
                    for i in result:
                        if i == []:
                            result.remove(i)
                    
                    for line in range(len(result)):
                        if line < len(result):
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
                                            num = result[line+1][a].replace('%','').replace(',','.')
                                            
                                            if float(num) > 0.5:
                                                
                                                if flag:
                                                    if not flagtext2:
                                                        message += '\nOKX\n'
                                                        flagtext2 = True
                                                    if not flagtext:
                                                        message += f'{result[0][0]}\n'
                                                        flagtext = True
                                                    message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
            elif spread_direction[0] and spread_direction[0] == 'Міжбіржові':
                if settings[0] and settings[0] and 'Binance' in settings[0] and 'ByBit' in settings[0]:
                    flagtext2 = False
                    
                    
                    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                    all_sheets = service.sheet.worksheets()
                    sh = all_sheets[1]

                    worksheet = service.sheet.worksheet(sh.title)
                    result = worksheet.get('A7:E9')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += 'Купуємо на ByBit продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                    
                    result = worksheet.get('A11:E13')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('A15:E17')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('A19:E21')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('A23:E25')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('A27:E29')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на ByBit продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                if settings[0] and 'Binance' in settings[0] and 'OKX' in settings[0]:
                    flagtext2 = False
                    
                    
                    service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                    all_sheets = service.sheet.worksheets()
                    sh = all_sheets[0]

                    worksheet = service.sheet.worksheet(sh.title)
                    result = worksheet.get('G7:K9')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += 'Купуємо на OKX продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                    
                    result = worksheet.get('G11:K13')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на OKX продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('G15:K17')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на OKX продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('G19:K21')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на OKX продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('G23:K25')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на OKX продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
                                                
                    result = worksheet.get('G27:K29')
                    
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
                                        num = result[line+1][a].replace('%','').replace(',','.')
                                        
                                        if float(num) > min_spread[0]:
                                            
                                            if flag:
                                                if not flagtext2:
                                                    message += '\nКупуємо на OKX продаємо на Binance\n'
                                                    flagtext2 = True
                                                if not flagtext:
                                                    message += f'{result[0][0]}\n'
                                                    flagtext = True
                                                message += f'{result[line][a]} {result[line+1][0]} +{num}%\n'
            elif spread_direction[0] and spread_direction[0] == 'Готівка':
                if settings[0] and 'Binance' in settings[0]:
                        flagtext2 = False
                        
                        
                        service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        all_sheets = service.sheet.worksheets()
                        sh = all_sheets[2]

                        worksheet = service.sheet.worksheet(sh.title)
                        result = worksheet.get('A10:E14')
                        
                        for i in result:
                            if i == []:
                                result.remove(i)
                        
                            
                        for row in range(len(result[0])):
                            cr = result[0][row].split(' ')
                            if cr[1] in settings[2]:
                                for line in range(len(result)):
                                    if line != 0:
                                        num = result[line][row]/1000
                                        if result[line][0] in settings[1] and num > min_spread[0]:
                                            if not flagtext2:
                                                message += '\Binance профіт\n'
                                                flagtext2 = True
                                            message += f'{result[line][0]}+ {result[0][row]}  +{num}%\n'
                if settings[0] and 'ByBit' in settings[0]:
                        flagtext2 = False
                        
                        
                        service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                        all_sheets = service.sheet.worksheets()
                        sh = all_sheets[2]

                        worksheet = service.sheet.worksheet(sh.title)
                        result = worksheet.get('G10:I14')
                        
                        for i in result:
                            if i == []:
                                result.remove(i)
                        
                            
                        for row in range(len(result[0])):
                            cr = result[0][row].split(' ')
                            if cr[1] in settings[2]:
                                for line in range(len(result)):
                                    if line != 0:
                                        num = result[line][row]/1000
                                        if result[line][0] in settings[1] and num > min_spread[0]:
                                            if not flagtext2:
                                                message += '\ByBit профіт\n'
                                                flagtext2 = True
                                            message += f'{result[line][0]}+ {result[0][row]}  +{num}%\n'                        
            elif spread_direction[0] and spread_direction[0] == 'Binance':
                service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                all_sheets = service.sheet.worksheets()
                sh = all_sheets[3]
                if 'Купуємо крипту, продаємо її' in settings[3]:
                    ranges = ['A69:J77','A58:K66','A80:J88','A91:J99','A102:J110','A113:J121','A124:J132','A135:J143','A146:J154','A157:J165','A168:J176']
                    for i in ranges:
                        mess = await parse_binance1(i,settings,min_spread)
                        message += mess
                if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' in settings[3]:
                    ranges = ['A192:F292','A295:F395','A398:F498','A501:F601','A604:F704','A707:F807']
                    for i in ranges:
                        mess = await parse_binance2(i,settings,min_spread)
                        message += mess
            elif spread_direction[0] and spread_direction[0] == 'OKX':
                service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                all_sheets = service.sheet.worksheets()
                sh = all_sheets[7]
                if 'Купуємо крипту, продаємо її' in settings[3]:
                    ranges = ['A22:F26','A28:E32','A34:E38','A40:E44','A46:E50','A52:E55']
                    for i in ranges:
                        mess = await parse_binance1(i,settings,min_spread)
                        message += mess
                if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' in settings[3]:
                    ranges = ['A60:C84','E60:G84','I60:K84']
                    for i in ranges:
                        mess = await parse_binance2(i,settings,min_spread)
                        message += mess
            elif spread_direction[0] and spread_direction[0] == 'ByBit':
                service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                all_sheets = service.sheet.worksheets()
                sh = all_sheets[8]
                if 'Купуємо крипту, продаємо її' in settings[3]:
                    ranges = ['A25:F29','A31:E35','A37:E41','A43:E47','A49:E53','A55:E59']
                    for i in ranges:
                        mess = await parse_binance1(i,settings,min_spread,sh.title)
                        message += mess
                if 'Купуємо крипту, міняємо на іншу, продаємо як мейкер' in settings[3]:
                    ranges = ['A63:C87','E63:G87','I63:K87']
                    for i in ranges:
                        mess = await parse_binance2(i,settings,min_spread,sh.title)
                        message += mess
            elif spread_direction[0] and spread_direction[0] == 'Wise':
                service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                all_sheets = service.sheet.worksheets()
                sh = all_sheets[9]
                if 'Купуємо крипту та продаємо (одна платіжна система)' in settings[9]:
                    ranges = ['A20:F25']
                    for i in ranges:
                        mess = await parse_binance3(i,settings,min_spread,sh.title)
                        message += mess
                if 'Купуємо крипту, конвертуємо на іншу та продаємо (одна платіжна система)' in settings[3]:
                    ranges = ['A30:E35','A37:E42','A44:E49','A50:E56']
                    for i in ranges:
                        mess = await parse_binance3(i,settings,min_spread,sh.title)
                        message += mess
            elif spread_direction[0] and spread_direction[0] == 'LocalBitcoins':
                service=GoogleSheets(filename='cred.json', google_sheet_name='TheBitok Table | 4975 Зв\'язок P2P')
                all_sheets = service.sheet.worksheets()
                sh = all_sheets[11]
                ranges = ['A19:C29']
                for i in ranges:
                    mess = await parse_binance2(i,settings,min_spread,sh.title)
                    message += mess
            
            if message:
                await bot2.send_message(user[1],message)  
            
        await asyncio.sleep(45)                                      

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
