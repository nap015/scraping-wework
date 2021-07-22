# scraping-wework

Web scraping freelance project, script scrapes inventory space for all WeWork buildings in NYC.
Current script not optimized for parallel scraping but will update in the future.

Result .csv file contains the following features in order:
State, City, Building Address, Inventory Code, Max Capacity (per each inventory space), reservation URL

.py file contains the runnable Python script, .ipynb file for development and preview.

* Required packages/libraries:
Selenium, bs4
