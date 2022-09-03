import ssl
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_info(url):
    try:
        print(">>> ", url)
        uh = urllib.request.urlopen(url,context=ctx)
        data = uh.read().decode()
        return BeautifulSoup(data, 'html.parser')
    except:
        print("Error from get_info function")
        quit()


def get_data(soup):
    try:
        new_data = soup.find_all("div", {"class": "col-xs-12 col-sm-12 col-md-4 grid-element"})
        dic = dict()
        for element in new_data:
            s = element.get_text(strip="\n")
            tag = element.find("a")
            t = tag.get("href")
            x = 0
            for i in range(len(t)):
                if t[len(t)-i-1] == '/':
                    break
                x += 1
            t = t[-x:]
            dic[t] = s
            print(t, s)
        return dic
    except:
        print("Error from get_data function")
        quit()


def chose():
    print("\nWybierz numer:")
    return input()


def write_data(my_data):
    s = ''
    for element in my_data:
        tag = element.find('p')
        term = tag.get_text()
        s += '\n' + '>>> ' + term + ':' + '\n'
        subject = element.find_all('td')
        for e in subject:
            try:
                x = e.find('div')
                s += x.get_text(strip='\n') + '\n'
            except:
                continue
    return s


# strona agh:
u = "https://sylabusy.agh.edu.pl/pl/1/2/18/1/4"

# wybór wydziału:
soup = get_info(u)
departments = get_data(soup)
u += '/' + chose()

# wybór kierunku:
soup = get_info(u)
majors = get_data(soup)
major = chose()
u += '/' + major

# kierunek -> zapis do pliku:
soup = get_info(u)
output = list()
for i in range(7, 14):
    new_data = soup.find_all("div", {"id": "syl-grid-period-" + str(i)})
    output.append(write_data(new_data))

try:
    name = majors[major] + '.txt'
except:
    name = "Syllabus.txt"

file = open(name, 'w')
print(majors)
print('    ', majors[major])
file.write('>>>' + majors[major] + ':')
file.write('\n\n')

for i in range(len(output)):
    print(output[i])
    file.write(output[i])
