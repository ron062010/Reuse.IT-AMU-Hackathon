# Reuse.iT
# Reuse iT or Lose iT.

This app aims to reduce the amount of waste produced at first place and even if waste is generated, ways to reuse it/dispose it properly will be given.
The app has two login options of 1. Personal User and 2. Dealer

User Side Interface

1. Object Recognition: The scrap item will be recognized through camera and ways to reuse/recycle it will be displayed along with the item’s Carbon Footprint. For this pre trained VGG16 model is used.
2. Donate to NGO:  This feature enables the user to donate the usable materials. List of all available NGOs will be displayed along with their contact details.
3. Waste Record: The user can keep a track of his personal scrap items. He can also upload a photo of the total scrap at his place and can send all these details to the specific dealer he wants which the dealer can see in his interface.
4. Nearby Drop-off Centers: The users will be provided with the list of the nearby drop-off centers which they can consider to recycle the scrap.


Scrap Dealer Side Interface

1. Nearby pick-up destinations: The dealer will be able to see the live requests made to collect the scrap items, by the user.
2. Shortest Route: In case of multiple pickup requests, this feature helps the dealer to decide the shortest route for his journey.
3. Rates: The dealer can view the photo uploaded by the user once a request has been made and he can send his rates accordingly to the user.

Tech Stack:

1. FrontEnd: HTML/CSS/Javascript
2. BackEnd: Flask
3. Database: MySQL
4. Object Recognition: Deep Learning (vgg16)
5. Shortest Path: Google Maps API
6. Automation: Selenium Bot


link for model.h5 file: https://drive.google.com/file/d/1dkjCAl_uqOsCmKAN82Qmj0KV8t7ep7lm/view?usp=sharing

link for dataset : https://drive.google.com/drive/folders/1RkPlpGGDQx5vjW1BW_qNLTRczvm6czvg?usp=sharing
