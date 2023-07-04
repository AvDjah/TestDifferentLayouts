from selenium import webdriver
import time
import json

driver = webdriver.Chrome()
driver.get("https://app.cloudqa.io/home/AutomationPracticeForm")
forms = driver.find_elements_by_css_selector("form")
for i in forms:
    print(i.get_attribute("id"))

# form1 = driver.find_element_by_id("nestedshadowdomautomationtestform")
# shadow = form1.find_element_by_css_selector("nestedshadow-form")
# driver.execute_script("console.log(arguments[0].shado)",shadow)
# out = driver.execute_script('return arguments[0].shadowRoot.querySelector("shadow-form").querySelector("#fname")', shadow)
# # print(shadow)
# # time.sleep(8)
# out.send_keys("hehehehehe")
# time.sleep(5)
# print(out)
# el = out.find_element_by_id("fname")
# driver.execute("arguments[0].scrollIntoView(true)",el)

f = driver.find_element_by_id("shadowdomautomationtestform")
print(f)
l = f.find_element_by_id("fname")
print(l.get_attribute("placeholder"))

driver.close()