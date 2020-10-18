from selenium import webdriver
from timeit import default_timer as timer
import psycopg2
from pprint import pprint
from datetime import datetime
from time import sleep
 
driver = webdriver.Chrome()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
start = timer()
driver.get("https://www.meijer.com/")
button_element = driver.find_element_by_id ("store-flyout-link-root")
end = timer()
time_taken = end-start
print(time_taken)
conn = psycopg2.connect('dbname=performance')
cur = conn.cursor()
today = datetime.now()
query = """
    INSERT INTO
        metrics
    VALUES
        (%s, %s)
    """
values = (time_taken, today)
cur.execute(query, values)
conn.commit()
conn.close()
driver.close()