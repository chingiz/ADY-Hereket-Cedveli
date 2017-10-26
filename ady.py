#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import os
import sys

import requests
from fabulous import text

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
    
from humanfriendly.tables import format_pretty_table
from fabulous.color import highlight_green, green, red, yellow


baku_header = [highlight_green('Qatar №-si'.decode("utf-8").strip()),
               green('Bakıdan çıxma'.decode("utf-8").strip()),
               green('Biləcəriyə çatma'.decode("utf-8").strip()),
               yellow('Biləcəridən getmə'.decode("utf-8").strip()),
               yellow('Xırdalana çatma'.decode("utf-8").strip()), red('Xırdalandan getmə'.decode("utf-8").strip()),
               red('Sumqayıta çatma'.decode("utf-8").strip())]

sum_header = [highlight_green('Qatar №-si'.decode("utf-8").strip()),
              green('Sumqayıtdan çıxma'.decode("utf-8").strip()),
              green('Xırdalana çatma'.decode("utf-8").strip()), yellow('Xırdalana getmə'.decode("utf-8").strip()),
              yellow('Biləcəriyə çatma'.decode("utf-8").strip()), red('Biləcəriyə getmə'.decode("utf-8").strip()),
              red('Bakıya çatma'.decode("utf-8").strip())]

baku_table = []
sum_table = []


def get_table():
    
    url = 'https://ady.az/az/tables/index/52/44'
    
    # Faking user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }  
    
    response = requests.get(url, verify=True, headers=headers)

    parsed_html = BeautifulSoup(response.content)

    modal12 = parsed_html.body.find(id="modal_12").table.text

    numbs = filter(lambda x: '0' <= x <= '9', modal12)
    c = 28
    while len(numbs) >= c:
        k = numbs[0:c]
        arr = []
        brr = []

        toggle = False
        
        while len(k) >= 4:
            st = k[0:4]
            if k[0] == '6':
                if int(k[2:4]) % 2 == 0:
                    toggle = False
                else:
                    toggle = True
            else:
                st = "     " + k[0:2] + ":" + k[2:4]
            if toggle:
                arr.append(st)
            else:
                brr.append(st)
            k = k[4:len(k)]
        if toggle:
            baku_table.append(arr)
        else:
            sum_table.append(brr)
        numbs = numbs[c:len(numbs)]


def main(argv):
    
    if argv == '-h' or argv == '--help':
        
        print(text.Text("ady", color='#0099ff', shadow=True, skew=5))
        print("ady -- Bakı -> Sumqayıt -> Bakı hərəkət cədvəli")
        print("ady ['-b', '--baku', '--bakı'] -- bakı üçün hərəkət cədvəli")
        print("ady ['-s', '--sum', '--sumgait', '--sumqayıt'] -- sumqayıt üçün hərəkət cədvəli")
        print("ady ['-a', '--all', '--ha', '--hamısı'] -- hər iki hərəkət cədvəli")
        
    else:
        
        get_table()
        
        if argv == "-b" or argv == "--baku" or argv == "--bakı":
            print(format_pretty_table(baku_table, baku_header))
            sys.exit()
            
        elif argv == "-s" or argv == "--sum" or argv == "--sumgait" or argv == "--sumqayıt":
            print(format_pretty_table(sum_table, sum_header))
            sys.exit()
            
        elif argv == "-a" or argv == "--all" or argv == "--ha" or argv == "--hamısı":
            print(format_pretty_table(baku_table, baku_header))
            print(format_pretty_table(sum_table, sum_header))
            sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 1:
        main(sys.argv[1])
    else:
        os.system("python ady.py -h")
