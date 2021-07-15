import json
import os
import sys
from src.spider import Spider

config_path = os.path.split(
    os.path.realpath(__file__))[0] + os.sep + 'config.json'
if not os.path.isfile(config_path):
    sys.exit(u'current path：%s does not exist config.json' %
                (os.path.split(os.path.realpath(__file__))[0] + os.sep))
with open(config_path, encoding = 'utf-8-sig') as f:
    config = json.loads(f.read())

spider = Spider(config)
spider.main()