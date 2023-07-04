from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
import time
import json


class CheckFields: 
    def __init__(self,driver) -> None:
        self.driver = driver

    def write_text(self,text,field):
        field.send_keys(text)
        time.sleep(1)
    
    def check_if_fields_present(self,form):
        try:
            el = form.find_element_by_id("fname")
            return el
        except:
            return None
        
    def check_for_nested(self, form, num) :
        start = "nestedshadow-form"
        nesting = str(num)
        if nesting.isdigit():
            curr = start + nesting
            nested = form.find_element_by_css_selector(curr)
            out = self.get_inner_shadow(curr,nested)
        else:
            nested = form.find_element_by_css_selector(start)
            out = self.get_final_shadow_form(start,nested)



    def get_inner_shadow(self,name,shadow):
        name = str(name)
        last = str(name[-1])
        start = "nestedshadow-form"
        if int(last) == 3:
            out = self.driver.execute_script('return arguments[0].shadowRoot.querySelector(arguments[1])', shadow, start)
            print(name,"->",start)
            return self.get_final_shadow_form(start,out)
            pass
        else :
            num = int(name[-1])
            newname = start + str(num-1)
            print(name,"->",start)
            out = self.driver.execute_script('return arguments[0].shadowRoot.querySelector(arguments[1])', shadow, newname)
            return self.get_inner_shadow(newname,out)


    def get_final_shadow_form(self,name,shadow):
        name = str(name)
        start = "nestedshadow-form"
        out = None
        if name.strip() == "nestedshadow-form":
            out = self.driver.execute_script('return arguments[0].shadowRoot.querySelector("shadow-form")', shadow)
            self.find_elements_and_write(out)
            print("Base Done!!!!")
            return out

        

    
    def get_forms_id_list(self,driver : WebDriver):
        forms_id_list = []
        forms_list = driver.find_elements_by_css_selector("form")
        for i in forms_list:
            if str(i).strip() != '':
                forms_id_list.append(i.get_attribute("id"))
        return forms_id_list
    


    def find_required_fields(self,form) :
        field = self.check_if_fields_present(form) 
        if  field == None:
            print("Not Found Fname")
            #Shadow Element Deal with IT
            id = form.get_attribute("id")
            nesting = str(id)
            self.check_for_nested(form,nesting[-1])
        else :
            print("Found Fname")
            self.find_elements_and_write(form)
        pass


    def process_each_form(self, id: str, driver: WebDriver):
        print(id)
        form_element = None
        try:
            form_element = driver.find_element_by_css_selector("#"+id)
        except:
            print("Error!!!!!!!!: "+id)
        
        if form_element != None :
            self.find_required_fields(form_element)

        


    def process_forms(self,forms_id_list : list[str], driver : WebDriver):
        for i in forms_id_list:
            self.process_each_form(i,driver)

            print("\n")


    def elements_to_fill(self):
        #Add the elements that you want to fill here
        dict = {}
        dict["fname"] = "Hellow"
        dict["lname"] = "World"
        dict["About"] = "Heelo This is automation"
        dict["Agree"] = True
        self.valdict = dict
        pass



    def find_elements_and_write(self,form : WebDriver):
        #Specify Cases for special elements
        print("Writing")
        for key,value in self.valdict.items():
            out = None
            if key == "About":
                out = form.find_element_by_css_selector("textarea")
            elif key == "Agree":
                try :
                    out = form.find_element_by_id(key)
                except :
                    out = None
                    try: 
                        print("Pas1")
                        out = form.find_element_by_css_selector("shadow-form")
                        self.driver.execute_script("console.log(arguments[0])",out)
                        #I need shadowroot
                        out = self.driver.execute_script("return arguments[0].shadowRoot.querySelector('#Agree')",out)
                    except:
                        #I am shadow-form
                        print("Pas2")
                        out = self.driver.execute_script("return arguments[0].shadowRoot.querySelector('#Agree')",form)
                    self.driver.execute_script("console.log(arguments[0])",form)
            else:
                out = form.find_element_by_id(key)

            if out == None: 
                print("Out issue in writing")
                continue

            if type(value) == str:
                out.send_keys(value)
            else:
                out.click()
            time.sleep(1)



if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://app.cloudqa.io/home/AutomationPracticeForm")
    # driver.fullscreen_window()
    tester = CheckFields(driver)
    tester.elements_to_fill()
    forms_list = tester.get_forms_id_list(driver)
    print(forms_list)
    tester.process_forms(forms_list,driver)
    time.sleep(5)
    # driver.close()


