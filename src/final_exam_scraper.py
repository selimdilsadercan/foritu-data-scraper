from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import re
import threading
from time import sleep

from scraper import Scraper
from logger import Logger
from constants import *
from driver_manager import DriverManager


class FinalExamScraper(Scraper):
    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.final_exams = []
        self.load_page(FINAL_EXAM_URL)

    def get_branch_codes(self):
        """Extract all available branch codes from the dropdown"""
        try:
            # Wait for the dropdown to load
            dropdown = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.ID, "DersBransKoduId"))
            )
            
            select = Select(dropdown)
            branch_codes = []
            
            for option in select.options:
                if option.get_attribute("value") and option.get_attribute("value") != "":
                    branch_codes.append({
                        'value': option.get_attribute("value"),
                        'text': option.text.strip()
                    })
            
            Logger.log_info(f"Found {len(branch_codes)} branch codes")
            return branch_codes
            
        except TimeoutException:
            Logger.log_error("Timeout waiting for branch codes dropdown to load")
            return []

    def scrape_exam_table(self, branch_code_info):
        """Scrape the exam table for a specific branch code"""
        try:
            # Select the branch code from dropdown
            dropdown = self.webdriver.find_element(By.ID, "DersBransKoduId")
            select = Select(dropdown)
            select.select_by_value(branch_code_info['value'])
            
            # Click the submit button
            submit_button = self.webdriver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Wait for the table to load
            self.wait(2)
            
            # Check if table container is visible
            table_container = self.webdriver.find_element(By.ID, "finalTakvimiTableContainer")
            if table_container.get_attribute("style") and "display: none" in table_container.get_attribute("style"):
                Logger.log_warning(f"No exam data found for branch code: {branch_code_info['text']}")
                return []
            
            # Find the table
            table = table_container.find_element(By.TAG_NAME, "table")
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            exam_data = []
            
            # Skip header row
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 10:  # Ensure we have all expected columns
                    exam_row = {
                        'crn': cells[0].text.strip(),
                        'course_code': cells[1].text.strip(),
                        'course_number': cells[2].text.strip(),
                        'course_name': cells[3].text.strip(),
                        'academician': cells[4].text.strip(),
                        'exam_type': cells[5].text.strip(),
                        'exam_location': cells[6].text.strip(),
                        'day': cells[7].text.strip(),
                        'time': cells[8].text.strip(),
                        'date': cells[9].text.strip(),
                        'branch_code': branch_code_info['text']
                    }
                    exam_data.append(exam_row)
            
            Logger.log_info(f"Scraped {len(exam_data)} exams for branch code: {branch_code_info['text']}")
            return exam_data
            
        except (TimeoutException, NoSuchElementException) as e:
            Logger.log_error(f"Error scraping exams for branch code {branch_code_info['text']}: {str(e)}")
            return []

    def scrape_branch_codes_thread_routine(self, branch_codes, thread_prefix, log_interval_modulo=10):
        """Thread routine for scraping multiple branch codes"""
        driver = DriverManager.create_driver()
        driver.get(FINAL_EXAM_URL)
        sleep(3)
        
        # Switch to Turkish if needed
        self.switch_to_turkish(driver, thread_prefix)
        
        thread_exams = []
        
        for i, branch_code in enumerate(branch_codes):
            try:
                # Create a new scraper instance for this thread
                thread_scraper = FinalExamScraper(driver)
                exams = thread_scraper.scrape_exam_table(branch_code)
                thread_exams.extend(exams)
                
                if (i + 1) % log_interval_modulo == 0:
                    Logger.log_info(f"{thread_prefix} Scraped {len(thread_exams)} exams so far")
                    
            except Exception as e:
                Logger.log_error(f"{thread_prefix} Error processing branch code {branch_code['text']}: {str(e)}")
        
        # Add thread results to main results
        self.final_exams.extend(thread_exams)
        
        Logger.log_info(f"{thread_prefix} Completed. Total exams scraped: {len(thread_exams)}")
        DriverManager.kill_driver(driver)

    def split_list_into_chunks(self, lst, num_chunks):
        """Split list into chunks for parallel processing"""
        chunk_size = len(lst) // num_chunks
        remainder = len(lst) % num_chunks
        
        chunks = []
        start = 0
        
        for i in range(num_chunks):
            end = start + chunk_size + (1 if i < remainder else 0)
            chunks.append(lst[start:end])
            start = end
        
        return chunks

    def scrape_final_exams(self):
        """Main method to scrape all final exams"""
        Logger.log_info("====== Scraping Final Exam Schedule ======")
        
        self.final_exams = []
        
        # Get all branch codes
        Logger.log_info("Getting branch codes...")
        branch_codes = self.get_branch_codes()
        
        if not branch_codes:
            Logger.log_error("No branch codes found. Cannot proceed with scraping.")
            return []
        
        Logger.log_info(f"Found {len(branch_codes)} branch codes to scrape")
        
        # Split into chunks for parallel processing
        chunks = self.split_list_into_chunks(branch_codes, MAX_THREAD_COUNT)
        threads = []
        
        for i in range(MAX_THREAD_COUNT):
            if chunks[i]:  # Only create thread if chunk has data
                prefix = f"[royal_blue1][Thread {str(i).zfill(2)}][/royal_blue1]"
                t = threading.Thread(target=self.scrape_branch_codes_thread_routine, args=(chunks[i], prefix))
                threads.append(t)
        
        # Start and wait for threads to finish
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        Logger.log_info(f"[bold green]Final exam scraping completed. Total exams scraped: {len(self.final_exams)}[/bold green]")
        return self.final_exams
