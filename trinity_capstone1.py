import requests

from abc import ABC, abstractmethod

from supabase import create_client, Client as SupabaseClient

import os
from dotenv import load_dotenv

from google import genai

load_dotenv()

# HI I AM APEX
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

class DatabaseSecure(ABC):
    @abstractmethod
    def InsertMarketData(self, data: str, price: int):
        pass

class TransmitionSecure(ABC):
    @abstractmethod
    def secure_message(self, data: str, phone: str):
        pass


class DatabaseWork(DatabaseSecure):
    def __init__(self):
        self.db: SupabaseClient = create_client(SUPABASE_URL, SUPABASE_KEY)
        
    def InsertMarketData(self, data: str, price: int):
        try:
           
            self.db.table('market_logs').insert({"data": data, "price": price}).execute()
            print(f"SUPABASE SUCCESS: Logged price {price} into the database table")
        except Exception as e:
            print(f"SUPABASE FAILURE: {e}")

    def FetchMarketData(self):
        try:
            logData = self.db.table('market_logs').select('*').execute()
            processedData = logData.data
            print(f'Data fetched from supabase: {processedData}')
            return processedData
        except Exception as e:
            print(f'supabase fetch failure: {e}')
        


class WhatsappAlert(TransmitionSecure):
    def __init__(self):
       
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    def secure_message(self, data: str, phone: str):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload={"chat_id":phone,"text":data}
            responce=requests.post(url,json=payload)
            if responce.status_code ==200:
                print(f"TELEGRAM SUCCESS: Message sent to Chat ID {phone}")
            else:
                print(f"TELEGRAM FAILURE: {responce.text}")
        except Exception as e:
            print(f"TELEGRAM FAILURE: The transmission was blocked. Error: {e}")
# NICE TO MEET YOU
class UnifiedMarketFunction:
    def __init__(self, db: DatabaseSecure, comms: TransmitionSecure, crop_type: str):
        self.db = db
        self.comms = comms
        self.crop_type = crop_type
        self.__crop_price = 0

        self.ai_client=genai.Client(api_key=GEMINI_API_KEY)
        
    def NewMarketPrice(self, price: int):
        if price < 0:
            print("The crop price is negative and is not valid")
            self.db.InsertMarketData(self.crop_type, price)
        else:
            self.__crop_price = price
            print(f"The crop price has been updated to {self.__crop_price} successfully")
            self.db.InsertMarketData(self.crop_type, price)
            
    def MarketAnalysis(self, phone: str):
        print("Initiating AI analysis")

        prompt=f"You are a professional agricultural financial advisor.give a text description on The current market price for {self.crop_type} is {self.__crop_price} rupees and the market is volatile and the database data is {self.db.FetchMarketData()}. Write a very brief, single-sentence recommendation on whether the farmer should sell now or hold, based on this price point."
        try:
            response=self.ai_client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
            )
            ai_advice=response.text
            print(f"AI ADVICE:{ai_advice}")

            self.comms.secure_message(ai_advice,phone)
        except Exception as e:
            print(f"AI ORCHESTRATION FAILED,REASON:{e}")    
# SEE YOU AGAIN
if __name__ == "__main__":
    print("INITIATING IRON BACKEND BOOT SEQUENCE")
    
    secure_db = DatabaseWork()
    main_gateway = WhatsappAlert()
    
    apex_node = UnifiedMarketFunction(secure_db, main_gateway, "lemon")
    
    print("\nSCENARIO: FLAWLESS EXECUTION")
    apex_node.NewMarketPrice(5)
    
 
    apex_node.MarketAnalysis("TELEGRAM_CHAT_ID")



    