#!/usr/bin/python
import requests
import argparse


tracker_url = 'http://www.17track.net/restapi/handlertrack.ashx'


headers = {
'Accept': '*/*',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Origin': 'http://www.17track.net',
'Referer': 'http://www.17track.net/pt/track?nums={package}&fc=0',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
}

form_data = '{{"guid":"","data":[{{"num":"{package}"}}]}}'

parser = argparse.ArgumentParser(description='Track any package on 17Track.net')
parser.add_argument('packages', type=str, action='append', help='packages to track')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--format', default='json', choices=['json', 'last_only'])
args = parser.parse_args()


package_list = args.packages


s = requests.Session()

for pack in package_list:
    lheaders = headers
    lheaders['Referer'] = lheaders['Referer'].format(package=pack)
    lform = form_data.format(package=pack)
    r = s.post(tracker_url, headers=lheaders, data=lform)

    if args.format == 'json':
        if args.verbose:
            print(r.json())
        else:
            d = {}
            data = r.json()
            for k in data['dat']:
                d['package'] = k['no']
                d['last_event'] = {}
                d['last_event']['date'] = k['track']['z0']['a']
                d['last_event']['location'] = k['track']['z0']['c']
                d['last_event']['message'] = k['track']['z0']['z']

                d['all_events'] = []
                for event in k['track']['z1']:
                    o = {}
                    o['date'] = event['a']
                    o['location'] = event['c']
                    o['message'] = event['z']
                    d['all_events'].append(o)
    elif args.format == 'last_only':
        d = {}
        data = r.json()
        for k in data['dat']:
            pno = k['no']
            pdate = k['track']['z0']['a']
            plocation = k['track']['z0']['c']
            pmessage = k['track']['z0']['z']
            print('{} - {} - {} - {}'.format(pno,pdate,plocation,pmessage))











