from selenium import webdriver
import lxml.html

class Scrape:
  site_url = 'https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a<eq_market_cap;'

  def load_chrome_driver(self):
    chromedriver_path = "E:/Utilities/chromedriver.exe"
    self.driver = webdriver.Chrome(chromedriver_path)
    self.driver.implicitly_wait(30)

  def scrape_details(self, url):
    self.driver.get(url)

    page_name = self.driver.find_elements_by_xpath('//h1[@itemprop="name"]')[0].text

    page = lxml.html.fromstring(self.driver.page_source)

    exchange = page.xpath('//div[@id="DropDownContainer"]//i[contains(@class, "btnTextDropDwn")]/text()')[0]

    valid_labels = [
      'Type',
      'Market',
      'ISIN',
      'CUSIP',
    ]

    small_table_data = {}
    for valid_label in valid_labels:
      labels = page.xpath('//div[@id="quotes_summary_current_data"]//div[@class="right"]//div/span[1][contains(text(), "%s")]/text()' % valid_label)
      data = []
      if valid_label != 'Market':
        data = page.xpath('//div[@id="quotes_summary_current_data"]//div[@class="right"]//div/span[1][contains(text(), "%s")]/following-sibling::span[1]/text()' % valid_label)
      else:
        data = page.xpath('//div[@id="quotes_summary_current_data"]//div[@class="right"]//div/span[1][contains(text(), "%s")]/following-sibling::span[1]/@title' % valid_label)

      if len(labels) > 0 and len(data) > 0:
        small_table_data[valid_label] = data[0]
      else:
        small_table_data[valid_label] = '-'

    industry = page.xpath('//div[@class="companyProfileHeader"]/div[contains(text(), "Industry")]/a/text()')[0]

    sector = page.xpath('//div[@class="companyProfileHeader"]/div[contains(text(), "Sector")]/a/text()')[0]

    valid_labels = [
      'Prev. Close',
      'Open',
      'Volume',
      'Average Vol. (3m)',
      '1-Year Change',
      'Day\'s Range',
      '52 wk Range',
      'Market Cap',
      'P/E Ratio',
      'Shares Outstanding',
      'Revenue',
      'EPS',
      'Dividend (Yield)',
      'Beta',
      'Next Earnings Date'
    ]

    data_below_figure = {}
    for valid_label in valid_labels:
      labels = page.xpath('//span[@class="float_lang_base_1" and contains(text(), "%s")]/text()' % valid_label)
      data = []
      if valid_label != 'Next Earnings Date':
        data = page.xpath('//span[@class="float_lang_base_1" and contains(text(), "%s")]/following-sibling::span[1]/text()' % valid_label)
      else:
        data = page.xpath('//span[@class="float_lang_base_1" and contains(text(), "%s")]/following-sibling::span[1]/a/text()' % valid_label)

      print(labels, data)

      if len(labels) > 0 and len(data) > 0:
        data_below_figure[valid_label] = data[0]
      else:
        data_below_figure[valid_label] = '-'


    print(page_name)
    print (exchange)
    print (small_table_data)
    print (industry, sector)
    print (data_below_figure)


  def run(self):
    self.load_chrome_driver()

    for index in range(200):
      url = self.site_url + str(index)
      self.driver.get(url)

      details_urls = self.driver.find_elements_by_xpath('//tbody//tr//td[@data-column-name="name_trans"]//a')

      for details in details_urls:
        self.scrape_details(details.get_attribute('href'))

task = Scrape()
task.run()