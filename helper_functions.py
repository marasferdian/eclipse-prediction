import ephem
from datetime import datetime, date, timedelta


def get_sun_moon_angular_radius(date_str):
    obs = ephem.Observer()
    obs.lon = '0'
    obs.lat = '0'
    obs.elevation = 0
    obs.date = date_str
    moon_pos = ephem.Moon(obs)
    sun_pos = ephem.Sun(obs)
    moon_radius_str = [float(x) for x in str(moon_pos.radius).split(":")]
    moon_radius = moon_radius_str[0] + moon_radius_str[1] / 60 + moon_radius_str[2] / 3600
    sun_radius_str = [float(x) for x in str(sun_pos.radius).split(":")]
    sun_radius = sun_radius_str[0] + sun_radius_str[1] / 60 + sun_radius_str[2] / 3600
    return sun_radius, moon_radius


def get_separation(date_str):
    obs = ephem.Observer()
    obs.lon = '0'
    obs.lat = '0'
    obs.elevation = 0
    obs.date = date_str
    moon_pos = ephem.Moon(obs)
    sun_pos = ephem.Sun(obs)
    separation_str = [float(token) for token in str(ephem.separation(moon_pos, sun_pos)).split(":")]
    separation = separation_str[0] + separation_str[1] / 60 + separation_str[2] / 3600
    # print(separation)
    return separation


def get_coordinates():
    coords = [str(lon) + ":" + str(lat) for lon in range(-170, 181, 10) for lat in range(-80, 81, 10)]
    coords.append("0:-90")
    coords.append("0:90")
    return coords


def calculate_diff_for_coords(coord, date_str):
    coords = coord.split(":")
    long = coords[0]
    lat = coords[1]
    obs = ephem.Observer()
    obs.lon = long
    obs.lat = lat
    obs.elevation = 0
    obs.date = date_str

    moon_pos = ephem.Moon(obs)
    sun_pos = ephem.Sun(obs)
    moon_radius_str = [float(x) for x in str(moon_pos.radius).split(":")]
    moon_radius = moon_radius_str[0] + moon_radius_str[1] / 60 + moon_radius_str[2] / 3600
    sun_radius_str = [float(x) for x in str(sun_pos.radius).split(":")]
    sun_radius = sun_radius_str[0] + sun_radius_str[1] / 60 + sun_radius_str[2] / 3600

    separation_str = [float(token) for token in str(ephem.separation(moon_pos, sun_pos)).split(":")]
    separation = separation_str[0] + separation_str[1] / 60 + separation_str[2] / 3600

    return moon_radius + sun_radius - separation


def check_if_any_coord_validate_eq(date_str):
    coordinates = get_coordinates()
    best = - 100000
    found = False
    best_coord = ''
    for c in coordinates:
        res = calculate_diff_for_coords(c, date_str)
        if res > -0.003 and res > best:
            found = True
            best = res
            best_coord = c
    return found, best, best_coord
