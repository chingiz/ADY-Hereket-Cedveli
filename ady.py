#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import requests
import os
import sys
import argparse

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


def getTable():
    url = 'https://ady.az/az/tables/index/52/44'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}  # faking user agent
    response = requests.get(url, verify=True, headers=headers)

    parsed_html = BeautifulSoup(response.content)

    modal12 = parsed_html.body.find(id="modal_12").table.text

    numbs = filter(lambda x: '0' <= x <= '9', modal12)
    c = 28
    while len(numbs) >= c:
        k = numbs[0:c]
        arr = []
        brr = []
        j = 0
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

def help():
    print(text.Text("ady", color='#0099ff', shadow=True, skew=5))
    print("ady -- Bakı -> Sumqayıt -> Bakı hərəkət cədvəli")
    print("ady ['baku'] -- bakı üçün hərəkət cədvəli")
    print("ady ['sum'] -- sumqayıt üçün hərəkət cədvəli")
    print("ady ['all'] -- hər iki hərəkət cədvəli")

def baku():
    getTable()
    print(format_pretty_table(baku_table, baku_header))

def sumgait():
    getTable()
    print(format_pretty_table(sum_table, sum_header))

def all():
    getTable()
    print(format_pretty_table(baku_table, baku_header))
    print(format_pretty_table(sum_table, sum_header))
    sys.exit()

def main():
    # Mapping arguments to function
    FUNCTION_MAP = {'help': help, 'baku' : baku, 'sumgait': sumgait, 'all': all}
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]

    # Execute
    func()

if __name__ == '__main__':
    main()
