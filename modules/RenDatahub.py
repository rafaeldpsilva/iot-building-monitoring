from bs4 import BeautifulSoup
from datetime import datetime
from utils import utils

def get_day_to_search_string():
    # Get the current date in the format 'YYYY-MM-DD'
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Construct the URL with the current date
    url = f'https://datahub.ren.pt/pt/homepage/electricity/production/detailed/?date={current_date}'


    # Send an HTTP GET request to the URL
    response = utils.update_values_get('get_day_to_search_string', url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with id="chart-1266"
        target_div = soup.find('div', {'id': 'chart-1266'})

        # Check if the div exists
        if target_div:
            # Extract the value of dayToSearchString from the data-id attribute
            data_id = target_div.get('data-id', '')
            day_to_search_string = None

            # Split the data-id attribute by '&' to separate parameters
            parameters = data_id.split('&')

            # Find the parameter containing dayToSearchString
            for param in parameters:
                if 'dayToSearchString' in param:
                    day_to_search_string = param.split('=')[1]
                    break
        else:
            print("Div with id='chart-1266' not found.")
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
    return day_to_search_string

def get_production_breakdown():
    day_to_search_string = get_day_to_search_string()
    url = f'https://datahub.ren.pt/service/Electricity/ProductionBreakdown/1266?culture=pt-PT&dayToSearchString={day_to_search_string}&isShare=true'
    
    production_breakdown = utils.update_values_post("production breakdown", url)
    
    legend = production_breakdown['xAxis']['categories']
    unit = production_breakdown['yAxis']['title']['text']
    label = []
    series = []
    for line in production_breakdown['series']:
        label.append(line['name'])
        series.append({"name": line['name'], "data": line['data']})
        
    return {"legend": legend, "unit": unit, "labels": label, "series": series}