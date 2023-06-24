import requests
import json



# response = requests.post(
#     "http://127.0.0.1:5000/ads/",
#     json={
#         'ad_title': 'title_1',
#         'ad_description': 'la la la ',
#         'ad_creator': 1},

# )


# response = requests.get("http://127.0.0.1:5000/ads/1")

# response = requests.delete("http://127.0.0.1:5000/ads/3")


# response = requests.patch(
#     "http://127.0.0.1:5000/ads/2",
#     json={
#         'ad_title': 'title_90',
#         },

# )



# response = requests.post("http://127.0.0.1:5000/registration/",
#                          json={
#                             "user_mail": "user_7",
#                             "user_password": "pass7"
 
#                          })




response = requests.get("http://127.0.0.1:5000/login/",
                        params={'mail': 'user_7',
                                'password': 'pass7'},
                                )








json_data = json.loads(response.text)
print(json_data)

