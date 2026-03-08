import requests
from datetime import datetime, timedelta
import os
import csv

def main():
    while True:
        print("\n-------Weather App-------\n""=========================\n")
        print("1. Search\n" "2. View History\n" "3. Clear History\n" "4. Exit\n")
        try:
            user_input = int(input("Enter option of your choice(1-4): "))
            if user_input == 1:
                api_key = # use openWeather to generate API key and paste it over this comment
                search = input("Enter City: ").lower().capitalize()
                handling_request_time_error(search, api_key)
            elif user_input == 2:
                delete = False
                load_to_csv(delete)
            elif user_input == 3:
                delete = True
                clear_history(delete)
            elif user_input == 4:
                print("Goodbye👋")
                exit()
            else:
                print("Invalid input. Please enter a number between 1 & 4")
        except ValueError:
            print("Invalid input. Please enter a number(1-4)")

def handling_request_time_error(search, api_key):
    while True:
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={search}&units=metric&appid={api_key}")

        if weather_data.json()['cod'] == '404':
            print("No City Found.")
            break
        timezone = weather_data.json()['timezone']
        local_time = datetime.utcnow() + timedelta(seconds=timezone)
        formatted_time = local_time.strftime("Date: %d %b, %Y on %a\n   Time: %H:%M:%S")

        weather_data_analysis(weather_data, formatted_time, search)
        break

def weather_data_analysis(weather_data, formatted_time, search):
    country = weather_data.json()['sys']['country']
    weather = weather_data.json()['weather'][0]['description']
    temp = round(weather_data.json()['main']['temp'])
    feels_like = round(weather_data.json()['main']['feels_like'])
    temp_max = round(weather_data.json()['main']['temp_max'])
    temp_min = round(weather_data.json()['main']['temp_min'])
    humidity = weather_data.json()['main']['humidity']

    print(f"\nCity Name: {search}\n"
        f"Country: {country}\n"
        f"The date and time in {search} is:\n   {formatted_time}\n"
        f"The Weather in {search} is: {weather}\n"
        f"The Temperature Today is: {temp}℃\n"
        f"It feels like: {feels_like}℃\n"
        f"The Highest Temperature is: {temp_max}℃\n"
        f"The Lowest Temperature is: {temp_min}℃\n"
        f"The Humidity Today is: {humidity}%")
    save_searches_to_list(search)

def save_searches_to_list(search):
    history_list.append(search)
    save_to_csv()
    return_back()

def save_to_csv():
    try:
        if history_list:
            with open(csv_file_path, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                if history_list:
                    csv_writer.writerow([history_list[-1]])
        else:
            f = open(csv_file_path, "w+")
            f.close()

    except Exception as e:
        print(f'An error occurred: {e}')
        return_back()

def load_to_csv(is_deleting):
    try:
        if not os.path.exists(csv_file_path):
            print("No history to be found.")
            return_back()
        if os.stat(csv_file_path).st_size == 0:
            print("No History to be found.")
            return_back()
        history_list.clear()

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            history_found = False
            for row in csv_reader:
                if len(row) == 1:
                    history = row[0]
                    history_list.append(history)
                    history_found = True

            if history_found and not is_deleting:
                print("\n--Search History--\n"
                      "==================\n")
                for idx, history in enumerate(history_list, start=1):
                    print(f"{idx}. {history}")
                return_back()

            elif history_found and is_deleting:
                return
            else:
                print("No valid history entries found.")
                return_back()
    except Exception as e:
        print(f"An Error has occurred: {e}")

def clear_history(is_deleting):
    while True:
        try:
            if not os.path.exists(csv_file_path):
                print("No history to be found.")
                return_back()
            if os.stat(csv_file_path).st_size == 0:
                print("History is empty.")
                return_back()
            user_choice = input("Do you want to clear history(y/n): ").lower()
            if user_choice == 'n':
                main()
            elif user_choice == 'y':
                delete = True
                load_to_csv(is_deleting)
                history_list.clear()
                save_to_csv()
                print("History cleared✅")
                return_back()
            else:
                print("Invalid input. please enter (y) or (n).")
        except Exception as e:
            print(f"An error occurred: {e}")

def return_back():
    input("\nPress enter to return: ")
    main()

if __name__ == '__main__':
    history_list = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "weather.csv")
    main()
