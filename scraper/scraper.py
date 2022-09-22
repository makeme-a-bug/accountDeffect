import random
import time
from typing import Dict,List,Any,Union
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from .utils import solve_captch
from rich.console import Console
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException , NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from dateutil.parser import parse
import pandas as pd

class Scraper(webdriver.Remote):

    def __init__(self,profile_name:str,profile_uuid:str, url:List[str], command_executor:str, destroy_browser:bool = False , tracker:List = [] ) -> None:
        self.command_executor = command_executor
        # self.capabilities = desired_capabilities
        self.profile_name = profile_name
        self.profile_uuid = profile_uuid
        self.url = url
        self.destroy_browser = destroy_browser
        self.console = Console()
        self.tracker = tracker
        self.current_page = 1

        super(Scraper,self).__init__(self.command_executor,desired_capabilities={})
        self.set_page_load_timeout(120)
        self.implicitly_wait(120)
        try:
            self.maximize_window()
        except:
            pass


    def get_data(self):
        """
        Starts reporting for the urls and profile given in the initial
        """
        data = "{}"
        if self.get_page(self.url):
            temp_data = self.get_json()
            data = temp_data
            
                    
        return data
        # self.quit()

    def bring_to_front(self):
        try:
            self.minimize_window()
        except:
            pass
        try:
            self.maximize_window()
        except:
            pass

    def get_json(self):
        self.bring_to_front()
        data = "{}"
        for i in range(3):
            try:
                WebDriverWait(self, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[href*='/messaging/inbox']")))
                ele = self.find_element(By.ID,"sc-content-container")
                data = ele.text
                break
            except TimeoutException:
                pass
        return data

    def get_page(self,url:str) -> None:
        """
        gets the url in the browser.\n
        parameters:\n
        url:<str>
        returns:\n
        None
        """
        url_open = False
        self.get(url)
        time.sleep(3)
        for i in range(3):
            try:
                captcha = self.solve_captcha()
                logged_in = self.is_profile_logged_in()
                if captcha and logged_in:
                    WebDriverWait(self, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[href*='/messaging/inbox']")))
                    url_open = True
                else:
                    pass
                break
            except TimeoutException:
                self.get(url)
        return url_open

    def solve_captcha(self) -> bool:
        """
        Checks if captcha appreared on the page.if appeared will try to solve it.
        return:
        True  : if captcha was solved
        False : if captcha was not solved
        """

        if "Try different image" in self.page_source:
            print(f"Captcha appear for profile [{self.profile_uuid}]")
            if not solve_captch(self):
                print(self.profile_name, "CAPTCHA not solved")
                return False
        return True
    
    def is_profile_logged_in(self) -> bool:
        """
        Checks if the multilogin is logged into amazon \n
        returns:\n
        True  : if the profile is logged in
        False : if the profile is not logged in
        """
        time.sleep(10)
        if "By continuing, you agree to Amazon's" not in self.page_source:
            return True
        self.console.log(f"{self.profile_name}:Profile not logged in into Amazon account",style='red')
        return False


    def __exit__(self, *args) -> None:
        if self.destroy_browser:
            self.quit()
            time.sleep(5)


