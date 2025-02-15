
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.lang import Builder 
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
import requests

Builder.load_file('style.kv')

class Style(MDAnchorLayout):

    def search(self):
        city_name = self.ids.sn.text 
        api_key = "d718df6a5fee036e83b46f1861242ce8"
        # api_key = "934bfed84c2365129fe9b7d811dde0ac"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(base_url)
            data = response.json()
            
            if data["cod"] != "404":
                self.update_ui(data)
            else:
                self.error()
        except:
            self.error()

    def update_ui(self, data):
        self.ids.sn.text = ''
        self.ids.nn.text = f"Location: {data['name']}"
        
        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        self.ids.st.text = f"Status: {weather}"
        self.ids.ht.text = f"HTemperature: {temp_max}°C"
        self.ids.lt.text = f"LTemperature: {temp_min}°C"
        self.ids.mo.text = f"Moisture: {humidity}%"
        self.ids.ws.text = f"WindSpeed: {wind_speed} m/s"
        
        # Set weather icons based on weather condition
        if weather == "Clear":
            self.ids.im.source = 'sunny.jpg'
            self.ids.n0.icon = 'weather-sunny'
        elif weather == "Clouds":
            self.ids.im.source = 'cloudy.jpeg'
            self.ids.n0.icon = 'weather-cloudy'
        elif weather == "Rain":
            self.ids.im.source = 'rainy.jpeg'
            self.ids.n0.icon = 'weather-rainy'

    def error(self):
        self.me = MDDialog(
            title='    Error ',
            text='You entered the wrong area or location name ' +
            '\n                                              or\n' +
            'The name of the region is not in the data',
            buttons=[
                MDRoundFlatButton(text=' close ', on_press=self.close_me),
                MDRoundFlatButton(text=' solution ', on_press=self.solu)
            ]
        )
        self.me.open()

    def close_me(self, obj):
        self.me.dismiss()

    def solu(self, obj):
        self.me.dismiss()
        self.ms = MDDialog(
            title=' Solution ',
            text='If you entered the correct name and it wasn`t listed ,' + '\n' +
            'Say the name of the area or location near your location \n',
            buttons=[MDRoundFlatButton(text=' close ', on_press=self.close_ms)]
        )
        self.ms.open()

    def close_ms(self, obj):
        self.ms.dismiss()

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.title = ' Weather '
        return Style()

Main().run()
