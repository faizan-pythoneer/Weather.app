from flask import Flask, render_template, request
import json
import urllib.request
import urllib.error

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'Lahore'
    
    api_key = 'd8a8cfa60c3024ef70c5130aff0cc064'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        with urllib.request.urlopen(url) as response:
            source = response.read()
            list_of_data = json.loads(source)
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "cityname": city,
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": f"{list_of_data['main']['temp']}°C",
                "temp_cel": f"{list_of_data['main']['temp']}°C",
                "pressure": f"{list_of_data['main']['pressure']} hPa",
                "humidity": f"{list_of_data['main']['humidity']}%",
            }
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code}")
        data = {"error": "City not found or API request failed."}
    except json.JSONDecodeError:
        print("Error decoding JSON")
        data = {"error": "Error decoding response."}
    except Exception as e:
        print(f"An error occurred: {e}")
        data = {"error": "An unexpected error occurred."}

    print(data)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
