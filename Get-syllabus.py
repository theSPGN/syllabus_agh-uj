import ssl
import urllib.error
import urllib.request
from datetime import date
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_info(url_syllabus):
    try:
        print(">>> ", url_syllabus)
        uh = urllib.request.urlopen(url_syllabus, context=ctx)
        data = uh.read().decode()
        return BeautifulSoup(data, "html.parser")
    except Exception as e:
        print("Error from get_info function: ", e)
        quit()


def get_data(my_data):
    try:
        look_for_data = my_data.find_all("div", {"class": "col-xs-12 col-lg-4"})
        dic = dict()
        for element in look_for_data:
            s = element.get_text(strip="\n")
            tag = element.find("a")
            t = tag.get("href")
            counter = 0
            for a in range(len(t)):
                if t[len(t) - a - 1] == "/":
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


def write_data(my_data, number):
    s = ""
    term_int = number - 7
    for element in my_data:
        term_int += 1
        try:
            tag = element.find("p")
            term = tag.get_text()
            if term.startswith("Semestr") is False:
                raise AttributeError
            term_add = ">>>" + term + ":"
        except AttributeError:
            term_add = ">>>" + "Semestr " + str(term_int) + ":"

        s += "\n" + term_add + "\n" + "\n"
        subject = element.find_all("td")
        for e in subject:
            try:
                tag = e.find("div")
                s += tag.get_text(strip="\n") + "\n"
            except AttributeError:
                continue
    return s


def main(do_want_to_print, u):
    # department choice
    soup = get_info(u)
    departments = get_data(soup)
    depart = chose()
    u += "/" + depart

    # field choice
    soup = get_info(u)
    majors = get_data(soup)
    major = chose()
    u += "/" + major

    # get information about courses
    soup = get_info(u)
    output = list()
    for i in range(7, 14):
        new_data = soup.find_all("div", {"id": "syl-grid-period-" + str(i)})
        output.append(write_data(new_data, i))

    # Saving to the file
    try:
        name = majors[major] + ".txt"
    except KeyError:
        name = "Syllabus.txt"
    file = open(name, "w")
    faculty = departments[depart].upper()
    field = majors[major].upper()
    file.write(">>> " + faculty + " <<<")
    file.write("\n>>> " + field + ":")
    file.write("\n\n")

    print(faculty + "\n" + field)  # field of science name printing
    for i in range(len(output)):
        if do_want_to_print is True:
            print(output[i])
        file.write(output[i])
    print("Courses have been saved in:", name)


def agh_link():
    url_agh = "https://sylabusy.agh.edu.pl/pl/1/2/"
    # actual year
    current_year = date.today().year - 2004
    try:
        url_agh += str(current_year)
        urllib.request.urlopen(url_agh)
    except WindowsError:
        try:
            url_agh = url_agh[0:-2]
            url_agh += str(current_year - 1)
            urllib.request.urlopen(url_agh)
        except WindowsError:
            url_agh = url_agh[0:-2]
            url_agh += "18"
    url_agh += "/"
    print("Wybierz rodzaj studiów:")
    print("1. Stacjonarne")
    print("2. Niestacjonarne")
    if input() == "2":
        url_agh += "2"
    else:
        url_agh += "1"
    print("Wybierz formę studiów:")
    print("1.inżynierskie")
    print("2.licencjackie")
    print("3.magisterskie inżynierskie")
    print("4.magisterskie")
    print("5.podyplomowe")
    url_agh += "/"
    form = input()
    if form == "5":
        url_agh = "https://sylabusy.agh.edu.pl/pl/1/2/18/1/6"  # there is no 'niestacjonarne' in 'podyplomowe'
    elif form == "4":
        url_agh += "2"
    elif form == "3":
        url_agh += "5"
    elif form == "2":
        url_agh += "1"
    else:
        url_agh += "4"

    return url_agh


def uj_link():
    url_uj = "https://sylabus.uj.edu.pl/pl/"
    current_year = date.today().year - 2017
    try:
        url_uj += str(current_year)
        urllib.request.urlopen(url_uj)
    except WindowsError:
        try:
            url_uj += str(current_year - 1)
            urllib.request.urlopen(url_uj)
        except WindowsError:
            url_uj += "5"
    url_uj += "/"
    print("Wybierz rodzaj studiów:")
    print("1. Stacjonarne")
    print("2. Niestacjonarne")
    if input() == "2":
        url_uj += "2"
    else:
        url_uj += "1"
    print("Wybierz formę studiów:")
    print("1.pierwszego stopnia")
    print("2.pierwszego stopnia, wspólne")
    print("3.drugiego stopnia")
    print("4.jednolite magisterskie")
    url_uj += "/"
    term = input()
    if term == "4":
        url_uj += "7"
    elif term == "3":
        url_uj += "3"
    elif term == "2":
        url_uj += "8"
    else:
        url_uj += "2"

    return url_uj


while True:
    x = input("Do you want me to print courses also in terminal? (choose)[Y/N]")
    if x == "Y" or x == "1" or x == "y":
        want_print = True
    else:
        want_print = False
    # AGH/UJ
    print("Do it for AGH/UJ (choose)[A/U]")
    y = input()

    if y == "U" or y == "u" or y == "2":
        pass
        url = uj_link()
    else:
        url = agh_link()

    main(want_print, url)
    response = input("Do you want to exit? [Y/N]")
    if response == "N" or response == "0" or response == "n":
        continue
    else:
        quit()
