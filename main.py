from selenium import webdriver
import time
import json





def evaluate_form(driver,form):
    try:
        first_name = form.find_element_by_id("fname")
    except:
        first_name = None
    last_name = form.find_element_by_id("lname")
    try:
        dob = form.find_element_by_id("dob")
    except:
        dob = None
    try:
        agree = form.find_element_by_id("Agree")
    except:
        agree = None

    button = form.find_elements_by_class_name("btn-primary")

    #Send Keys
    if first_name != None:
        first_name.send_keys("Arvind")
    if last_name != None:
        last_name.send_keys("meena")
    if dob != None:
        dob.send_keys("1999-10-10")
    if agree != None:
        agree.click()

    time.sleep(3)
    #click submit
    for i in button :
        value = i.get_attribute("value")
        if value == "submit":
            i.click()
            break
    time.sleep(5)
    if driver.current_url != "https://app.cloudqa.io/Home/AutomationPracticeForm":
        print("Error")
        return
    result = driver.find_element_by_css_selector("pre")
    if result != None:
        json_result = json.loads(result.get_attribute("textContent"))
        print(json_result)





if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://app.cloudqa.io/home/AutomationPracticeForm")

    # Get the list of available forms
    forms_list = driver.find_elements_by_css_selector("form")
    form_ids = []
    for i in forms_list:
        print(i.get_attribute("id"))
        form_ids.append(i.get_attribute("id"))
    
    for i in form_ids:
        time.sleep(2)
        forms_list = driver.find_elements_by_css_selector("form")
        form = None
        print("Current: ",i)
        if i == "automationtestform":
            continue
        for j in forms_list: 
            if j.get_attribute("id") == i:
                form = j
        if form == None:
            print("Not Found: ",i)
            continue
        form = driver.find_element_by_id(i)
        evaluate_form(driver,form)
        if driver.current_url != "https://app.cloudqa.io/home/AutomationPracticeForm":
            driver.back()
    
