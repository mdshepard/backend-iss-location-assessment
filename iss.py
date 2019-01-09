import requests
import argparse
import sys
import time
import turtle

iss_url = 'http://api.open-notify.org/iss-now.json'
iss_over_url = 'http://api.open-notify.org/iss-pass.json'


def astronauts():
    r = requests.get('http://api.open-notify.org/astros.json')

    print('Total number of astronauts in space: '
          + str(len(r.json()['people'])))

    for person in r.json()['people']:
        print 'Astronaut: ' + person['name']
        print 'Spacecraft: ' + person['craft']
    print ''
    print ''


def iss_locator():
    r = requests.get(iss_url)
    r.encoding = 'ascii'
    result = r.json()
    location = result['iss_position']
    lat_raw = location['latitude']
    lon_raw = location['longitude']
    lat = float(lat_raw)
    lon = float(lon_raw)
    print('Latitude:', lat)
    print('Longitude:', lon)

    world = turtle.Screen()
    world.bgpic('map.gif')
    world.setup(720, 360)
    world.setworldcoordinates(-180, -90, 180, 90)

    world.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)

    iss.penup()
    iss.goto(lon, lat)
    world.exitonclick()


def overhead_locator():
    lat_over = 39.76
    lon_over = -86.15
    url = iss_over_url + '?lat=' + str(lat_over) + '&lon=' + str(lon_over)
    r = requests.get(url)
    result = r.json()

    world = turtle.Screen()
    world.bgpic('map.gif')
    world.setup(720, 360)
    world.setworldcoordinates(-180, -90, 180, 90)

    indy = result['response'][1]['risetime']
    iss_over = turtle.Turtle()
    iss_over.penup()
    iss_over.color('yellow')
    iss_over.goto(lon_over, lat_over)
    iss_over.dot(7)
    iss_over.hideturtle()
    style = ('Arial', 10, 'bold')
    iss_over.write(time.ctime(indy), font=style)
    world.exitonclick()


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--astronauts',
                        help='Lists astronauts and their spacecraft',
                        action='store_true')
    parser.add_argument('-i', '--iss',
                        help='Shows the current location of the ISS',
                        action='store_true')
    parser.add_argument('-o', '--overhead',
                        help='Tells when the ISS will be over Indianapolis',
                        action='store_true')

    return parser


def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    if parsed_args.astronauts:
        astronauts()
    elif parsed_args.iss:
        iss_locator()
    elif parsed_args.overhead:
        overhead_locator()
    else:
        parser.print_usage()


if __name__ == '__main__':
    main(sys.argv[1:])
