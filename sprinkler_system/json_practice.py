# Ryland Price
import json

current_info = {"first_section": 1, "second_section": 2, "third_section": 3,
                "fourth_section": 4, "fifth_section": 5, "sixth_section": 6, "section_1_time": 1, "section_2_time": 1,
                "section_3_time": 1, "section_4_time": 1, "section_5_time": 1, "section_6_time": 1}
with open("data_file.txt", "w") as file:
    file.write(json.dumps(current_info))

