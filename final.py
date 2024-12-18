import requests
import telegram
import datetime
import asyncio
import os

now = datetime.datetime.now()
current = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)

# 개인정보
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY")
# 특정 채팅방 ID 설정 (개인 Chat ID)
CHAT_ID = os.getenv("CHAT_ID")



lang = "kr"

full_url = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&q={CITY}&appid={API_KEY}&lang={lang}&units=metric"

response_org = requests.get(full_url).json()
#print(response_org['list'])
#print("###################################\n\n")
#print(response_org['list'][0])
#print("###################################\n\n")

"""
temp = response_org['list'][0]['main']['temp']
temp_min = response_org['list'][0]['main']['temp_min']
temp_max = response_org['list'][0]['main']['temp_max']
humidity = response_org['list'][0]['main']['humidity']
description = response_org['list'][0]['weather'][0]['description']
dt_txt = response_org['list'][0]['dt_txt']
pressure = response_org['list'][0]['main']['pressure']
"""

"""
print("온도: ", temp)
print("최저 온도: ", temp_min)
print("최고 온도: ", temp_max)
print("습도: ", humidity)
print("날씨: ", description)
print("기압: ", pressure)
print("시간: ", dt_txt)
print("########################################\n\n")
"""

# 날씨 데이터 리스트 추출
weather_list = response_org['list']
# 비동기 함수 정의
async def send_weather_update():
    bot = telegram.Bot(token=ACCESS_TOKEN)
    # 메시지 생성
    message = f"현재({current}) {CITY}의 날씨 정보입니다:\n\n"
    for i, weather in enumerate(weather_list[:5]):  # 향후 5개의 데이터만 가져오기
        dt_txt = weather['dt_txt']
        temp = weather['main']['temp']
        temp_min = weather['main']['temp_min']
        temp_max = weather['main']['temp_max']
        humidity = weather['main']['humidity']
        description = weather['weather'][0]['description']
        pressure = weather['main']['pressure']

        # 각 시간대별 메시지 추가
        message += (
            f"시간: {dt_txt}\n"
            f" - 온도: {temp}°C\n"
            f" - 최저/최고 온도: {temp_min}/{temp_max}°C\n"
            f" - 습도: {humidity}%\n"
            f" - 기압: {pressure} hPa\n"
            f" - 날씨: {description}\n\n"
        )

    # 메시지를 Telegram으로 전송
    await bot.send_message(chat_id=CHAT_ID, text=message)

# 비동기 함수 실행
asyncio.run(send_weather_update())