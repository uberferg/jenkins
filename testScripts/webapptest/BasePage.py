from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import hashlib
import random
import time


class BasePage:
    @property
    def cur_page_url(self):
        return self.driver.current_url

    @property
    def cur_page_title(self):
        return self.driver.title

    @property
    def cur_page_source(self):
        return self.driver.page_source

    @property
    def cur_page_source_hash(self):
        return hashlib.md5(self.driver.page_source.encode('utf-8')).hexdigest()

    def __init__(self, test):
        self.driver = test.driver

        self.TIMEOUT = 2

        self.prev_page_url = ""
        self.step_name = ""
        self.page_title = ""
        self.base_url = ""
        self.page_url = ""

        self.log_path = test.log_path
        self.screenshot_path = test.screenshot_path

    def find_by(self, **kwargs):
        elems = None

        try:
            if "id" in kwargs.keys():
                WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.ID, kwargs["id"])))
                elems = self.driver.find_element_by_id(kwargs["id"])
            else:
                for key, val in sorted(kwargs.items(), key=lambda x: x[0]):
                    if key == "name":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.NAME, val)))
                            elems = self.driver.find_elements_by_name(val)
                        else:
                            elems = elems.find_elements_by_name(val)
                    elif key == "link_text":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.LINK_TEXT, val)))
                            elems = self.driver.find_elements_by_link_text(val)
                        else:
                            elems = elems.find_elements_by_link_text(val)
                    elif key == "partial_link_text":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.PARTIAL_LINK_TEXT, val)))
                            elems = self.driver.find_elements_by_partial_link_text(val)
                        else:
                            elems = elems.find_elements_by_partial_link_text(val)
                    elif key == "tag_name":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.TAG_NAME, val)))
                            elems = self.driver.find_elements_by_tag_name(val)
                        else:
                            elems = elems.find_elements_by_tag_name(val)
                    elif key == "class_name":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.CLASS_NAME, val)))
                            elems = self.driver.find_elements_by_class_name(val)
                        else:
                            elems = elems.find_elements_by_class_name(val)
                    elif key == "css":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.CSS_SELECTOR, val)))
                            elems = self.driver.find_elements_by_css_selector(val)
                        else:
                            elems = elems.find_elements_by_css_selector(val)
                    elif key == "xpath":
                        if elems is None:
                            WebDriverWait(self.driver, self.TIMEOUT).until(
                                EC.visibility_of_any_elements_located((By.XPATH, val)))
                            elems = self.driver.find_elements_by_xpath(val)
                        else:
                            elems = elems.find_elements_by_xpath(val)
                    else:
                        pass

                    if len(elems) == 1:
                        return elems[0]
        except Exception as e:
            self.__add_to_log("Element not found: " + str(kwargs) + "\n")

        return elems

    def __human_type(self, elem, text):
        for char in text:
            time.sleep(random.uniform(0.05, 0.2))
            elem.send_keys(char)

    def __perf_action(self, elem, value=""):
        if elem is None:
            return

        self.exec_js("arguments[0].scrollIntoView(true);", elem)

        value = value.lower()
        tag_name = str(elem.get_attribute('tagName')).lower()

        if tag_name == "select":
            for option in elem.find_elements_by_tag_name('option'):
                if option.get_attribute("value").lower() == value:
                    option.click()
                    break
        elif tag_name == "textarea":
            elem.clear()
            elem.send_keys(value)
        elif tag_name == "div":
            if elem.get_attribute("role") in "slider":
                move = ActionChains(self.driver)
                arr = value.split(",")
                move.click_and_hold(elem).move_by_offset(int(arr[0]) * int(arr[1]), 0).release().perform()
            else:
                elem.click()
        elif tag_name == "iframe":
            pass
        elif tag_name == "input":
            type = elem.get_attribute('type').lower()
            if type in ("button", "submit"):
                if "bootstrap-touchspin-" in elem.className:
                    self.exec_js("return $(arguments[0]).trigger('mousedown').trigger('touchcancel');", elem)
                else:
                    elem.click()
            elif type in ("text", "password"):
                elem.clear()
               #elem.send_keys(value, Keys.ARROW_DOWN)
                self.__human_type(elem, value)
            elif type in ("radio", "checkbox"):
                elem.click()
            else:
                elem.click()
        else:
            elem.click()

    def _(self, elem, value="", step_name=""):
        if elem is not None:
            self.__add_to_log(self.__get_description(elem, value, step_name))

            self.__perf_action(elem, value)

    def switch_to(self, obj="", obj_name=""):
        if obj == "window":
            if obj_name in range(0, 9):
                self.driver.switch_to.window(self.driver.window_handles[obj_name])
            else:
                self.driver.switch_to.window(obj_name)
        elif obj == "alert":
            self.driver.switch_to.alert()
        elif obj == "active_elem":
            self.driver.switch_to.active_element()
        elif obj == "frame":
            self.driver.switch_to.frame(obj_name)
        elif obj == "p_frame":
            self.driver.switch_to.parent_frame(obj_name)
        else:
            self.driver.switch_to.default_content()

    def exec_js(self, js, elem):
        self.driver.execute_script(js, elem)

    def __get_description(self, elem, value="", step_name=""):
        if elem is None:
            return

        out = "\t"

        if self.prev_page_url != self.cur_page_url:
            self.prev_page_url = self.cur_page_url
            out = self.cur_page_url + "\n" + out
        if step_name != self.step_name:
            self.step_name = step_name
            out = self.step_name + "\n" + out

        value = value.lower()
        tag_name = str(elem.get_attribute('tagName')).lower()

        if tag_name == "a":
            out += "Click '" + elem.get_attribute('innerText').strip() + "' link"
        elif tag_name == "select":
            out += "Select '" + value + "' in '" + self.get_label(elem) + "' dropdown"
        elif tag_name == "textarea":
            out += "Enter '" + value + "' into '" + self.get_label(elem) + "' field"
        elif tag_name == "button":
            out += "Click '" + elem.get_attribute('innerText').strip() + "' button"
        elif tag_name == "div":
            if elem.get_attribute("role") in "slider":
                out += "Move slider '" + self.get_label(elem) + "' by " + value.split(",")[0].strip()
            else:
                out += "Click unknown element, tagName=" + elem.tag_name
        elif tag_name == "iframe":
            pass
        elif tag_name == "input":
            type = elem.get_attribute('type').lower()

            if type in ("button", "submit"):
                out += "Click '" + elem.get_attribute('value').strip() + "' button"
            elif type in ("text", "password"):
                out += "Enter '" + value + "' into '" + self.get_label(elem) + "' field"
            elif type in "radio":
                out += "Click '" + self.get_label(elem) + "' radio button"
            elif type in "checkbox":
                if elem.is_selected():
                    out += "Uncheck '" + self.get_label(elem) + "' check box"
                else:
                    out += "Check '" + self.get_label(elem) + "' check box"
            else:
                out += "Click unknown element, tagName=input, type=" + type
        else:
            out += "Click unknown element, tagName=" + elem.tag_name

        return out + "\n"

    def __add_to_log(self, text):
        with open(self.log_path, "a") as log:
            log.write(text)

    def get_label(self, elem):
        max_depth = 2

        if elem.get_attribute('type') == 'text':
            max_depth = 5

        t_elem = elem
        labels = self.driver.find_elements_by_css_selector("label[for=" + elem.get_attribute('id') + "]")

        while len(labels) == 0 and max_depth > 0:
            t_elem = t_elem.find_element_by_xpath("..")

            labels = t_elem.find_elements_by_xpath("./label")

            max_depth -= 1

        if labels is not None:
            return labels[0].get_attribute("innerText").strip()
        else:
            return ""

    def make_screenshot(self, path=""):
        if path == "":
            self.driver.save_screenshot(self.screenshot_path)
        else:
            self.driver.save_screenshot(path)
