from DataFrameAppend import *
from datetime import date
import platforma

DEFAULT_SIZES = [
    {
        "brand": "Hankook",
        "size": "195/65R15",
        "season(zima,lato,wielosezon)": "zima",
        "indeks nosnosci": "91",
        "indeks predkosci": "T",
        "bieznik(nieobowiazkowy)": "W452",
        "min. sztuk": "20",
        "min_dot": 2019,
        "type": "PCR",
    },
]

today = date.today()

try:
    with open(SIZES_FILE) as fp:
        temp_df = pandas.read_excel(SIZES_FILE, dtype="str")
        temp_df["min_dot"] = temp_df["min_dot"].astype(int)
        sizes = temp_df.to_dict("records")
except FileNotFoundError:
    sizes = DEFAULT_SIZES



LOGIN_SITE = "https://platformaopon.pl/"
CREDENTIALS_FILE = "credentials.txt"
SIZES_FILE = "sizes.xlsx"

driver = webdriver.Firefox()
driver.get(LOGIN_SITE)

with open(CREDENTIALS_FILE) as fp:
    credentials = fp.read().splitlines()

username_field = driver.find_element_by_xpath("//input[contains(@id, 'username')]")
password_field = driver.find_element_by_xpath("//input[contains(@id, 'password')]")
save_me_tick = driver.find_element_by_xpath("//span[contains(@class, 'tick halflings')]")
submit_field = driver.find_element_by_xpath("//input[contains(@id, 'submit')]")

username_field.send_keys(credentials[0])
password_field.send_keys(credentials[1])
save_me_tick.click()
submit_field.click()
sleep(4)

results = []
for size in sizes:
    results.extend(platforma.collect_data(size, today))

driver.find_element_by_xpath("//a[contains(@title, 'Wyloguj')]").click()
driver.close()

df = DataFrameAppend(results, columns = [
    "size",
    "pattern",
    "seller",
    "price",
    "stock",
    "dot",
    "remarks",
    "delivery",
    "date",
    "brand",
    "type",
    "season",
    ],
                     )

df.append_to_excel("data.xlsx", index=False)
