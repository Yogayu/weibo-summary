#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import random
from cookies import cookies
from user_agents import agents


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        print("cookies")
        # request.cookies = [{'SUB': '_2A250ESxsDeRhGeNI6FsT9SnFzDuIHXVXZxqkrDV_PUNbm9BeLUfMkW-YpwFKhz9PP7lTFbOpsDKBPY7S4A..', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WW0gfEoKnSTECvITeWGdCM35NHD95QfSoe4eo-N1KMNWs4Dqcjdi--ci-zRi-zRi--RiK.ci-8Wi--ci-zRiKL2', 'ALF': '1526108092', 'SCF': 'AjHYIYlQ8qUu7jMBhGx784xootiG-FjZBL2jmFhtC9cUMO4neuELg3BUNXFyYWHghTLnDBd1AKraDHkzrXVNzcw.', 'ALC': 'ac%3D2%26bt%3D1494572092%26cv%3D5.0%26et%3D1526108092%26ic%3D-632881178%26scf%3D%26uid%3D5639257977%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D4f73c3c2ecc9195f62706cfde9ec395f', 'sso_info': 'v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLWNo4y5jKOUt46TnLeJp5WpmYO0tY2jjLmMo5S3jpOctw==', 'tgc': 'TGT-NTYzOTI1Nzk3Nw==-1494572092-gz-A3177BBD59C373A60B557D74D801A1AD-1', 'LT': '1494572092'}]
        cookie = random.choice(cookies)
        print(cookie)
        request.cookies = cookie
