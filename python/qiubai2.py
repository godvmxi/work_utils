__author__ = 'bluebird'
#!/usr/bin/env python
#-*-encoding=utf-8 -*-
import urllib2
import re
URL = 'http://www.qiushibaike.com/hot/page/'
#first = re.compile(r'<div class="content"[^>]*>.*?(?=</div>)')
first = re.compile(r'<div class="content".*?(?=</div>)')
second = re.compile(r'(?<=>).*')

def main():
   recCount = 5
   total = 1
   ipage = 1
   while True:
       content = urllib2.urlopen(URL + str(ipage)).readlines()
       alls = ''
       for s in content:
           alls += s.strip()
       #print first.findall(alls)
       ipage+=1
       fs = first.findall(alls)
       thispage = [second.findall(s.strip())[0] for s in fs if s]
       for i, p in enumerate(thispage):
           print total,' ',p
           total += 1
           if (i + 1) % recCount == 0:
               raw_input('\nPress Key To Start More\n')
       ipage+=1

if __name__ == '__main__':
    main()
