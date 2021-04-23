import ephem


def get_positions(date_str):
    obs = ephem.Observer()
    obs.lon = '0'
    obs.lat = '0'
    obs.elevation = 0
    obs.date = date_str
    moon_pos = ephem.Moon(obs)
    sun_pos = ephem.Sun(obs)
    return moon_pos.alt, moon_pos.az, sun_pos.alt, sun_pos.az


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


def get_minimum_separation(date_str):
    min_sep = 10000
    obs = ephem.Observer()
    longitudes = ['0', '90', '180', '270']
    latitudes = ['0', '45', '-45']
    obs.elevation = 0
    hours = [(str(x) + y) for x in range(24) for y in [':00:00']]
    for lon in longitudes:
        for lat in latitudes:
            for h in hours:
                obs.date = date_str + ' ' + h
                obs.lon = lon
                obs.lat = lat
                moon_pos = ephem.Moon(obs)
                sun_pos = ephem.Sun(obs)
                separation_str = [float(token) for token in str(ephem.separation(moon_pos, sun_pos)).split(":")]
                separation = separation_str[0] + separation_str[1] / 60 + separation_str[2] / 3600
                if separation < min_sep:
                    min_sep = separation
    return min_sep


def get_minimum_separation_lunar(date_str):
    min_sep = 10000
    obs = ephem.Observer()
    longitudes = ['0', '90', '180', '270']
    latitudes = ['0', '45', '-45']
    obs.elevation = 0
    hours = [(str(x) + y) for x in range(24) for y in [':00:00']]
    for lon in longitudes:
        for lat in latitudes:
            for h in hours:
                obs.date = date_str + ' ' + h
                obs.lon = lon
                obs.lat = lat
                moon_pos = ephem.Moon(obs)
                sun_pos = ephem.Sun(obs)
                separation_str = [float(token) for token in str(ephem.separation(moon_pos, sun_pos)).split(":")]
                separation = separation_str[0] + separation_str[1] / 60 + separation_str[2] / 3600
                separation = min(abs(separation - 180), abs(separation + 180))
                if separation < min_sep:
                    min_sep = separation
    return min_sep


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


def calculate_diff_for_coords_lunar(coord, date_str):
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

    separation_str = [float(token) for token in str(ephem.separation(moon_pos, sun_pos)).split(":")]
    separation = separation_str[0] + separation_str[1] / 60 + separation_str[2] / 3600

    return min(abs(separation - 180), abs(separation + 180))


def is_initial_separation_condition_valid(date_str):
    c = '0:0'
    date_str = date_str + ' 12:00:00'
    sep = get_separation(date_str)
    return sep < 30


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


def check_if_any_coord_validate_eq_lunar(date_str):
    coordinates = get_coordinates()
    best = 100000
    found = False
    best_coord = ''
    for c in coordinates:
        res = calculate_diff_for_coords_lunar(c, date_str)
        if res < 0.56 and res < best:
            found = True
            best = res
            best_coord = c
    return found, best, best_coord


def convert_to_decimal_degrees(degrees_str):
    deg = [float(token) for token in degrees_str.split(":")]
    dec_deg = deg[0] + deg[1] / 60 + deg[2] / 3600
    return dec_deg
