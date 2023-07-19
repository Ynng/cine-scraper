from selenium import webdriver

# create a webdriver instance
driver = webdriver.Chrome()

# go to the desired URL
driver.get("https://www.cineplex.com/movie/oppenheimer-the-imax-experience-in-70mm-film")

# enable javascript
driver.execute_script("return navigator.webdriver")

# get the date range the movie is available
date_range = driver.find_element_by_class_name("movie-details__date-range").text

# print the date range
print(date_range)

# close the browser
driver.quit()
