import astropy
import ephem
import pandas as pd
from sunpy.map.maputils import solar_angular_radius
from pyephem_sunpath.sunpath import sunpos, sunpos_radiance
from datetime import datetime, date, timedelta
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time

from sunpy.coordinates import frames, sun

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
    radius_str = [float(x) for x in str(moon_pos.radius).split(":")]
    radius = radius_str[0] + radius_str[1] / 60 + radius_str[2] / 3600
    print("Moon: " + str(start_date) + " " + str(radius))
    # obs_time = datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S')
    # c = SkyCoord(0 * u.arcsec, 0 * u.arcsec, obstime=obs_time,
    #              observer="earth", frame=frames.Helioprojective)
    # equator = EarthLocation(lat=0 * u.deg, lon=0 * u.deg, height=0 * u.km)
    # frame_altaz = AltAz(obstime=Time(obs_time), location=equator)
    # sun_altaz = c.transform_to(frame_altaz)
    # print(f'Altitude is {sun_altaz.T.alt} and Azimuth is {sun_altaz.T.az}')

    start_date += delta
