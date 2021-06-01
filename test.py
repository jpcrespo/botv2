import pyowm

owm = pyowm.OWM("5191c33b7b0079d23ef33dfee00d6084")
mgr = owm.weather_manager()

sf = mgr.weather_at_place('la paz, Bolivia')

w = sf.weather
# ax=w.temperature('celsius')
print(w.temperature('celsius'))
