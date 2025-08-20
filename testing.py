from playwright.sync_api import sync_playwright

def get_links():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.facebook.com/marketplace/memphis/search/?query=cannondale%20caadx&minPrice=300&maxPrice=1000")

        # x out the login info 
        if page.locator('div[aria-label="Close"]'):
            # Click on the element once it's found
            page.locator('div[aria-label="Close"]').first.click()

        # time.sleep(10)

        # find all elements with role="link"
        links = page.locator('[role="link"]')

        # extract both inner texts and href URLs into lists
        texts = []
        urls = []
        for i in range(links.count()):
            link_element = links.nth(i)
            text = link_element.inner_text()
            if len(text.split('\n')) <= 1:
                continue
            href = "facebook.com" + link_element.get_attribute('href')

            if len(text.split('\n')) > 3:  # if price dropped, two prices are listed. keep dropped price only
                price, _, title, location = text.split('\n')
            elif len(text.split('\n')) == 3:
                price, title, location = text.split('\n')
            else:
                print("Error parsing text from listing", text)
                continue

            print(price, title, location)
            texts.append([price, title, location])
            urls.append(href)


        browser.close()

get_links()