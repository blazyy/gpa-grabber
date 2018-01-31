
# only works for one university currently. duh.

from selenium import webdriver
import csv

RRN = 160071601000
grades = []
credits = []
x = 1
creditPerSubject = [3, 3, 4, 3, 1, 1, 1, 1, 4, 3]
names = []
gpas = []
rrns = []


def grades_to_credits():
    for grade in grades:
        if grade == 'S':
            credits.append(10)
        elif grade == 'A':
            credits.append(9)
        elif grade == 'B':
            credits.append(8)
        elif grade == 'C':
            credits.append(7)
        elif grade == 'D':
            credits.append(6)
        elif grade == 'E':
            credits.append(5)
        else:
            credits.append(0)


def calc_gpa():
    totalcredits = 0
    i = 0
    for credit in credits:
        totalcredits += (credit * creditPerSubject[i])
        i += 1
    return totalcredits/24


# loads an instance of chrome, and then web page is loaded
driver = webdriver.Chrome()
driver.get('https://bsauniv.com/campit/result/sRespub.aspx?Frm=Regular')

while RRN < 160071602050:

    errorFound = ''

    # gets the input element
    rrnInput = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtRRNNumber')
    submit = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnGetResults')  # gets the submit button

    rrnInput.clear()  # in case something is already entered
    rrnInput.send_keys(RRN)  # loads in RRN
    submit.click()  # simulates a click

    try:
        errorFound = driver.find_element_by_id('validok_ctl00_ContentPlaceHolder1_TMessageBox1').text

        # if error found, click the 'OK' button, increment RRN, go back to start of loop
        if not errorFound:
            rrn_not_found_button_ok = driver.find_element_by_id('validok_ctl00_ContentPlaceHolder1_TMessageBox1')
            rrn_not_found_button_ok.click()
            RRN += 1
            continue
    except:
        x = 2

    name = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lblName')
    rrn = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lblRRN')
    RRN += 1

    for i in driver.find_elements_by_tag_name('td'):  # note to self: find a more efficient way of scanning the page.
        if len(i.text) < 2 and i.text.isalpha():
            grades.append(i.text)

    grades_to_credits()
    gpa = calc_gpa()

    rrns.append(rrn.text)  # appends rrn to list of rrns
    names.append(name.text.title())  # appends name to list of names
    gpas.append(gpa)  # you get the idea

    del grades[:]  # deletes current grade list so that next person's gpa can be calculated
    del credits[:]  # same as above

rows = zip(rrns, names, gpas)

with open("grades.csv", "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
        
