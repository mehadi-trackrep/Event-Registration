import copy
import time
import json
import gspread
import pandas as pd
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and access the Google Sheets data
def authenticate_and_get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials_bak.json', scope)
    client = gspread.authorize(creds)

    # Replace this with your actual Google Sheets link
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1K--9Z6NJ1EaHMVwrLWp605qU53A1DnEbocQtHWDpUwg').sheet1
    return sheet

# Fetch data from Google Sheets
def fetch_data():
    sheet = authenticate_and_get_sheet()
    data = sheet.get_all_records()  # Gets all the data as dictionaries
    return pd.DataFrame(data)

# Plotting the chart
def plot_chart(data):
    
    ## display top 10 batches:-
    batch_counts_t = data['SSC Batch'].value_counts()
    cnt = 0

    print("\n###এখন পর্যন্ত TOP 10 BATCHES:- ###\n")
    
    for k, v in dict(batch_counts_t).items():
        print(f"{cnt+1}) _{int(k)}_ - *{int(v)}* জন।")
        cnt += 1
        if cnt == 10: break

    user_input = 1
    while user_input:

        user_input = int(
            input(
"""
1) Enter 1 if we want to see batch wise sort plot\n
2) or enter 2 if we want to see frequency wise sort plot\n
3) else enter 0:-
"""
            )
        )
        
        if user_input:
            batch_counts = None
            if user_input == 1:
                ## Count the frequency of each SSC Batch and sort batch wise
                batch_counts = data['SSC Batch'].value_counts().sort_index()
            else:
                ## Count the frequency of each SSC Batch and sort frequency wise
                batch_counts = data['SSC Batch'].value_counts().sort_values()

            ## Plot the data
            plt.figure(figsize=(10, 6))
            batch_counts.plot(kind='bar') # ,rot=0, color="b"
            plt.title('Frequency of SSC Batches')
            plt.xlabel('SSC Batch')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()

            plt.show(block=False)

            ui = str(input("Input y if want to close the graph: ")).strip()
            if ui == "y":    
                plt.pause(3)
                plt.close()

package_to_count_map = {
    'বাবা': 1,
    'মা': 1,
    'স্বামী/স্ত্রী': 1,
    '১ জন বাচ্চা': 1,
    '২ জন বাচ্চা': 2,
    '৩ জন বাচ্চা': 3,
    '১ জন গেস্ট': 1,
    '২ জন গেস্ট': 2,
    '৩ জন গেস্ট': 3
}

# tshirt_cnt_map = {
#     'S': 0,
#     'M': 0,
#     'L': 0,
#     'XL': 6,
#     'XXL': 0,
#     'XXXL': 0
# }

tshirt_cnt_map = {
    'S': 2,
    'M': 6,
    'L': 29+4,
    'XL': 10+13,
    'XXL': 1,
    'XXXL': 0
}

def get_total_count(data, running_students):
    guests_c = data['গেস্ট প্যাকেজসমূহ*'].value_counts()
    guests_o = data['গেস্ট প্যাকেজসমূহ**'].value_counts()

    guests_cnt = 0

    for k, v in dict(guests_c).items():
        if k:
            k_splitted = [each_item.strip() for each_item in k.split(",") if each_item.strip()]
            for splitted_k in k_splitted:
                cnt = package_to_count_map[splitted_k]
                guests_cnt += (cnt * int(v))

    for k, v in dict(guests_o).items():
        if k:
            k_splitted = [each_item.strip() for each_item in k.split(",") if each_item.strip()]
            for splitted_k in k_splitted:
                cnt = package_to_count_map[splitted_k]
                guests_cnt += (cnt * int(v))

    print(f"@announcement\n")
    print(f"প্রাক্তন শিক্ষার্থী রেজিস্ট্রেশন সংখ্যাঃ {len(data) - running_students}")
    print(f"বর্তমান রানিং শিক্ষার্থী রেজিস্ট্রেশন সংখ্যাঃ {running_students}")
    print(f"(( *প্রাক্তন এবং রানিং শিক্ষার্থী সহ রেজিস্ট্রেশন সংখ্যা* )): *_{len(data)}_*")
    print(f"** গেস্ট রেজিস্ট্রেশন সংখ্যাঃ {guests_cnt}")
    print(f"===============================")
    print(f"এখন পর্যন্ত সর্বমোট অংশগ্রহণকারীর সংখ্যাঃ *_{len(data) + guests_cnt}_*\n")
    print(f"বিঃদ্রঃ এর বাইরে বুথেও কিছু আছে, অনলাইন হচ্ছে। 🚀🚀🚀\n\n\t\t'সৌহার্দ্য সম্প্রীতির বন্ধনে\n\t\tএসো স্মৃতিময় প্রাঙ্গণে'")


def get_total_tshirt_count(data):
    tshirt = data['টিশার্ট সাইজ']
    tshirt_g = data['Guest-T-shirts'] # geuest t-shirts

    for _, row in data.iterrows():
        the_column_value = row['টিশার্ট সাইজ']
        if the_column_value:
            k_splitted = [each_item.strip() for each_item in the_column_value.split(",") if each_item.strip()]
            for splitted_k in k_splitted:
                tshirt_size = splitted_k.strip().upper()
                tshirt_cnt_map[tshirt_size] += 1

    print(f"tshirt__freq: {data['টিশার্ট সাইজ'].value_counts()}")
    print(f"==> tshirt_cnt_map: {json.dumps(tshirt_cnt_map, indent=4)}")
    print(f"--> Total count 1: {sum(tshirt_cnt_map.values())}")


    for _, row in data.iterrows():
        the_column_value = row['Guest-T-shirts']
        if the_column_value:
            k_splitted = [each_item.strip() for each_item in the_column_value.split(",") if each_item.strip()]
            for splitted_k in k_splitted:
                tshirt_size = splitted_k.strip().upper()
                tshirt_cnt_map[tshirt_size] += 1

    print(f"tshirt_g__freq: {data['Guest-T-shirts'].value_counts()}")
    print(f"--> tshirt_cnt_map: {json.dumps(tshirt_cnt_map, indent=4)}")
    print(f"--> Total count 2(final): {sum(tshirt_cnt_map.values())}")
    

def main():
    data = fetch_data()
    df = copy.deepcopy(data)

    running_students = data['SSC Batch'].value_counts()[2025]
    get_total_count(data, running_students)
    
    df = df.drop(df[df['SSC Batch'] == 2025].index)
    plot_chart(df)

    get_total_tshirt_count(data)

if __name__ == '__main__':
    main()