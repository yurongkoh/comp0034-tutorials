import requests
from selenium import webdriver
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Implicit wait for 2 seconds
# driver.implicitly_wait(2)

# def test_server_live(dash_duo):
#     """
#     GIVEN the app is running
#     WHEN an HTTP request to the home page is made
#     THEN the HTTP response status code should be 200
#     """

#     # Start the app in a server
#     app = import_app(app_file="student.dash_single.paralympics_dash")
#     dash_duo.start_server(app)

#     # Delay to wait 2 seconds for the page to load
#     dash_duo.driver.implicitly_wait(2)

#     # Get the url for the web app root
#     # You can print this to see what it is e.g. print(f'The server url is {url}')
#     url = dash_duo.driver.current_url

#     # Requests is a python library and here is used to make an HTTP request to the sever url
#     response = requests.get(url)

#     # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
#     assert response.status_code == 200


# # def test_home_h1_text_equals(dash_duo):
#     """
#     GIVEN the app is running
#     WHEN the home page is available
#     THEN the H1 heading with an id of 'title' should have the text "Paralympics Dashboard"
#     """
#     # As before, use the import_app to run the Dash app in a threaded server
#     app = import_app(app_file="student.dash_single.paralympics_dash")
#     dash_duo.start_server(app)

#     # Wait for the H1 heading to be available on the page, timeout if this does not happen within 4 seconds
#     dash_duo.wait_for_element("h1", timeout=4)  # Dash function version

#     # Find the text content of the H1 heading element
#     h1_text = dash_duo.find_element("h1").text  # Dash function version

#     # Assertion checks that the heading has the expected text
#     assert h1_text == "Paralympics Dashboard"


# # def test_dropdown_selector(dash_duo):
#     """
#     GIVEN the app is running
#     WHEN the home page is available
#     THEN the id of 'dropdown-input' should have one of the expected values (events, sports, countries)
#     """
#     # As before, use the import_app to run the Dash app in a threaded server
#     app = import_app(app_file="student.dash_single.paralympics_dash")
#     dash_duo.start_server(app)

#     # Wait for the H1 heading to be available on the page, timeout if this does not happen within 4 seconds
#     dash_duo.wait_for_element("#dropdown-input", timeout=4)  # Dash function version

#     # Find the text content of the H1 heading element
#     value = dash_duo.find_element("#dropdown-input").get_attribute("value")  # Dash function version

#     # Assertion checks that the heading has the expected text
#     assert value == "events"


def test_bar_chart_updates(dash_duo):
    """
    GIVEN the app is running
    AND the checkboxes are present on the page
    AND a bar chart is present on the page
    WHEN both checkboxes are selected
    THEN the two charts should be in the div with the id 'bar-div' (can be tested with the class=dash-graph)
    """

    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait until the checkbox element is displayed
    dash_duo.wait_for_element("#checklist-input", timeout=4)
    dash_duo.wait_for_element("#checklist-input > div:nth-child(2) > label", timeout=4)

    # Find div with the id 'bar-div' that contains the charts
    bar_div = dash_duo.find_element("#bar-div")

    # count the number of elements in bar_div with the class 'dash-graph'
    num_charts_before = len(bar_div.find_elements_by_class_name("dash-graph"))

    # Select the 'Winter' checkbox. Summer is already selected by default.
    # dash_duo.find_element(By.CSS_SELECTOR("input[type='checkbox']")[0]).click()
    # wait_for_element_by_id('#checklist-input', timeout=4)
    # element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "checklist-input")))
    # wait_for_page(url=None, timeout=10)
    dash_duo.find_element('#checklist-input > div:nth-child(2) > label').click()
    #checklist-input > div:nth-child(2) > label
    #checklist-input > div:nth-child(2) > label

    # Click the checkbox
    # dash_duo.find_element("#Winter").click()

    # Wait 2 seconds for the bar chart to update
    dash_duo.driver.implicitly_wait(2)

    # Find div with the id 'bar-div' that contains the charts again
    bar_div = dash_duo.find_element("#bar-div")

    # count the number of elements in bar_div with the class 'dash-graph'
    num_charts_after = len(bar_div.find_elements_by_class_name("dash-graph"))

    # There should be 2 charts now and 1 at the start so you can assert that num_charts_after > num_charts_before
    assert num_charts_after > num_charts_before
