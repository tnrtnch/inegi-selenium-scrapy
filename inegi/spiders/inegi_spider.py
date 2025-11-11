import scrapy
import yaml
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from inegi.items import InegiItem

class InegiSpider(scrapy.Spider):
    name = "inegi_spider"
    allowed_domains = ["www3.inegi.org.mx"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("scraper.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.output_file = self.config.get("output_file", "sanctions.json")


        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def start_requests(self):
        yield scrapy.Request(url=self.config["target_url"], callback=self.parse_with_selenium)

    def parse_with_selenium(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()

        self.wait.until(EC.element_to_be_clickable((By.ID, "cphContenido_rbtNombre"))).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "cphContenido_txtNombre")))
        self.wait.until(EC.element_to_be_clickable((By.ID, "cphContenido_txtNombre"))).send_keys(
            self.config["search_query"]
        )
        self.wait.until(EC.element_to_be_clickable((By.ID, "cphContenido_lnkbtnTotal"))).click()
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//tbody)[5]//a")))

        yield from self.parse_page()

    def parse_page(self):
        while True:
            all_profiles = self.driver.find_elements(By.XPATH, "(//tbody)[5]//a[contains(@id,'lnkSancionar')]")
            for i in range(len(all_profiles)):
                all_profiles = self.driver.find_elements(By.XPATH, "(//tbody)[5]//a[contains(@id,'lnkSancionar')]")
                all_profiles[i].click()

                name_part = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//caption//span[@class='Etiqueta']"))
                ).text
                name = re.split(r'\bproveedor \b', name_part)[-1].strip()

                numbers = [
                    n.text.strip()
                    for n in self.driver.find_elements(By.XPATH, "//tr[@style='background-color:#EFEFEF;']/td[2]")
                    if n.text.strip()
                ]

                item = InegiItem()
                item["Entity_name"] = name
                item["Sanction_numbers"] = numbers
                yield item

                self.driver.back()
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, "(//tbody)[5]//a[contains(@id,'lnkSancionar')]")
                ))
            break

    def closed(self, reason):
        if hasattr(self, "driver") and self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed.")
