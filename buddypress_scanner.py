from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import math

'''
REQUIREMENTS:
    python3
    urllib.request
    bs4
    math

AUTHOR:
    Javo
'''

target = "https://example.com"
max_groups = 200
members_per_page = 10000
user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"


def get_members(url, groups, page_count):
    members = []
    for group in groups:
        members_url = str(url + "/groups/" + group + "/members/")
        print("Fetching: " + members_url)
        req = Request(members_url, headers={'User-Agent': user_agent})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        try:
            forum_members_count = soup.find(id='members').find('span').decode_contents().replace(",", "")
            print("The group has " + str(forum_members_count) + " members")
            members_url_page = members_url + "?mlpage=1&num=" + str(page_count)
            print("Fetching member page: " + members_url_page)
            req = Request(members_url_page, headers={'User-Agent': user_agent})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, "html.parser")
            links = soup.find_all('a', href=True)
            for link in links:
                href = link["href"]
                i = href.find("members/")
                if i >= 0:
                    href = href[i + 8:len(href) - 1]
                    if href != "" and href.find("?mlpage=") < 0 and not href in members:
                        members.append(href)

        except:
            print("! '" + group + "' is private group. Need an account to access it.")

    members = list(dict.fromkeys(members))
    members.sort()
    return members


def get_groups(url):
    groups = []
    try:
        req = Request(url, headers={'User-Agent': user_agent})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if "groups/" in href:
                i = href.find("groups/")
                if i >= 0:
                    href = href[i + 7:len(href) -1]
                    if href != "" and href.find("?grpage=1") < 0:
                        groups.append(href)

        groups = list(dict.fromkeys(groups))
        groups.sort()

    except:
        print("ERROR: Could not connect to the url")

    return groups


groups = get_groups(target + "/groups/?grpage=1&num=" + str(max_groups))
print("Found " + str(len(groups)) + " groups")
for group in groups:
    print(group)

if len(groups) > 0:
    members = get_members(target, groups, members_per_page)
    print("Total users found " + str(len(members)) + " users")
    for member in members:
        print(member)
