
import ephem
from datetime import datetime, date, timedelta

start_date = date(2012, 11, 1)
end_date = date(2100, 11, 30)
delta = timedelta(days=1)
while start_date <= end_date:
    obs = ephem.Observer()
    obs.lon = '0'
    obs.lat = '0'
    obs.elevation = 0
    obs.date = datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S')
    moon_pos = ephem.Moon(obs)
    sun_pos = ephem.Sun(obs)
    moon_radius_str = [float(x) for x in str(moon_pos.radius).split(":")]
    moon_radius = moon_radius_str[0] + moon_radius_str[1] / 60 + moon_radius_str[2] / 3600
    print("Moon: " + str(start_date) + " " + str(moon_radius))
    sun_radius_str = [float(x) for x in str(sun_pos.radius).split(":")]
    sun_radius = sun_radius_str[0] + sun_radius_str[1] / 60 + sun_radius_str[2] / 3600
    print("Sun: " + str(start_date) + " " + str(sun_radius))

    start_date += delta
