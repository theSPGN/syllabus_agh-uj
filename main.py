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
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        return BeautifulSoup(data, 'html.parser')
    except Exception as e:
        print("Error from get_info function: ", e)
        quit()


def get_data(my_data):
    try:
        look_for_data = my_data.find_all("div", {"class": "col-xs-12 col-sm-12 col-md-4 grid-element"})
        dic = dict()
        for element in look_for_data:
            s = element.get_text(strip="\n")
            tag = element.find("a")
            t = tag.get("href")
            counter = 0
            for a in range(len(t)):
                if t[len(t) - a - 1] == '/':
                    break
                counter += 1
            t = t[-counter:]
            dic[t] = s
            print(t, s)
        return dic
    except Exception as e:
        print("Error from get_data function:", e)
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
                tag = e.find('div')
                s += tag.get_text(strip='\n') + '\n'
            except AttributeError:
                continue
    return s


def main(do_want_to_print):
    # strona agh:
    u = "https://sylabusy.agh.edu.pl/pl/1/2/18/1/4"

    # wybór wydziału:
    soup = get_info(u)
    departments = get_data(soup)
    depart = chose()
    u += '/' + depart

    # wybór kierunku:
    soup = get_info(u)
    majors = get_data(soup)
    major = chose()
    u += '/' + major

    # kierunek -> pobranie danych (przedzmiotów):
    soup = get_info(u)
    output = list()
    for i in range(7, 14):
        new_data = soup.find_all("div", {"id": "syl-grid-period-" + str(i)})
        output.append(write_data(new_data))

    # Zapis do plku:
    try:
        name = majors[major] + '.txt'
    except KeyError:
        name = "Syllabus.txt"
    file = open(name, 'w')
    file.write('>>>' + departments[depart])
    file.write('\n>>>' + majors[major] + ':')
    file.write('\n\n')

    print(departments[depart] + '\n' + majors[major])  # nazwa kierunku
    for i in range(len(output)):
        if do_want_to_print is True:
            print(output[i])
        file.write(output[i])
    print("Courses have been saved in:", name)


x = input('Do you want me to print courses also in terminal? (choose)[Y/N]')
if x == 'Y' or x == '1' or x == 'y':
    want_print = True
else:
    want_print = False
main(want_print)
