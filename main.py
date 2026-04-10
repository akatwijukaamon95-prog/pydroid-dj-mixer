from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader

class DJDeck(BoxLayout):
    def __init__(self, deck_name, default_file, **kwargs):
        super().__init__(orientation='vertical', spacing=10, **kwargs)
        self.sound = None
        self.filename = default_file
        self.is_killed = False 
        
        self.add_widget(Label(text=deck_name, font_size='24sp', color=(0.1, 0.7, 1, 1)))
        
        self.btn = Button(text="LOAD & PLAY", size_hint_y=0.4)
        self.btn.bind(on_press=self.toggle_playback)
        self.add_widget(self.btn)
        
        self.filter_btn = Button(text="BASS KILL", background_color=(0.3, 0.3, 0.3, 1))
        self.filter_btn.bind(on_press=self.toggle_filter)
        self.add_widget(self.filter_btn)
        
        self.gain_slider = Slider(min=0, max=1, value=1.0, size_hint_y=0.2)
        self.add_widget(self.gain_slider)

    def toggle_playback(self, instance):
        if not self.sound:
            self.sound = SoundLoader.load(self.filename)
            
        if self.sound:
            if self.sound.state == 'stop':
                self.sound.play()
                self.btn.text = "STOP"
            else:
                self.sound.stop()
                self.btn.text = "PLAY"

    def toggle_filter(self, instance):
        self.is_killed = not self.is_killed
        if self.is_killed:
            instance.background_color = (1, 0.5, 0, 1)
            if self.sound: self.sound.volume = 0.2 
        else:
            instance.background_color = (0.3, 0.3, 0.3, 1)
            if self.sound: self.sound.volume = self.gain_slider.value

class MainMixer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10)
        
        self.decks_layout = GridLayout(cols=2, spacing=40, size_hint_y=0.7)
        self.deck_a = DJDeck(deck_name="DECK A", default_file="track1.mp3")
        self.deck_b = DJDeck(deck_name="DECK B", default_file="track2.mp3")
        
        self.decks_layout.add_widget(self.deck_a)
        self.decks_layout.add_widget(self.deck_b)
        self.add_widget(self.decks_layout)
        
        self.add_widget(Label(text="CROSSFADER", size_hint_y=0.05))
        self.crossfader = Slider(min=0, max=1, value=0.5, size_hint_y=0.2)
        self.crossfader.bind(value=self.update_mix)
        self.add_widget(self.crossfader)

    def update_mix(self, instance, value):
        if self.deck_a.sound and not self.deck_a.is_killed:
            self.deck_a.sound.volume = (1 - value) * self.deck_a.gain_slider.value
        if self.deck_b.sound and not self.deck_b.is_killed:
            self.deck_b.sound.volume = value * self.deck_b.gain_slider.value

class PydroidDJ(App):
    def build(self):
        return MainMixer()

if __name__ == '__main__':
    PydroidDJ().run()
      
