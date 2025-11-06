from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_socketio import SocketIO
from extensions import db
from models import db, User, Place, PlaceImage, LikedPlace
import os
import sys
import subprocess
import logging

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "ashborn"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

db.init_app(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from routes import *

def insert_places():
    with app.app_context():
        db.session.query(PlaceImage).delete()
        db.session.query(Place).delete()
        db.session.commit()

        places = [
            {"name": "Bhadrakali Temple", "description": "An ancient temple dedicated to Goddess Kali located in Warangal, known for its spiritual atmosphere and history.", "state": "Telangana"},
            {"name": "Medak Fort", "description": "A hidden architectural gem in Telangana offering a blend of nature, history, and stunning views.", "state": "Telangana"},
            {"name": "Pocharam Wildlife Sanctuary", "description": "A quiet sanctuary near Medak, ideal for nature lovers and bird watchers.", "state": "Telangana"},

            {"name": "Lambasingi", "description": "Known as the 'Kashmir of Andhra Pradesh', Lambasingi is a misty, cold hill station lesser-known to tourists.", "state": "Andhra Pradesh"},
            {"name": "Maredumilli", "description": "A forest destination known for waterfalls and tribal culture, great for eco-tourism.", "state": "Andhra Pradesh"},
            {"name": "Gandikota", "description": "Often called the 'Grand Canyon of India', it's a beautiful gorge formed by the Penna River.", "state": "Andhra Pradesh"},

            {"name": "Tarkarli", "description": "A coastal village known for clear beaches, scuba diving, and peaceful surroundings.", "state": "Maharashtra"},
            {"name": "Chikhaldara", "description": "The only coffee-growing region in Maharashtra, it's a cool and quiet hill station.", "state": "Maharashtra"},
            {"name": "Bhandardara", "description": "A serene getaway with waterfalls, lakes, and forts near Igatpuri.", "state": "Maharashtra"},

            {"name": "Saputara", "description": "A small hill station on the Maharashtra-Gujarat border offering a peaceful environment and tribal culture.", "state": "Gujarat"},
            {"name": "Zarwani Waterfalls", "description": "A quiet natural retreat near the Shoolpaneshwar Wildlife Sanctuary.", "state": "Gujarat"},
            {"name": "Polo Forest", "description": "An offbeat historical and nature destination surrounded by dense forest.", "state": "Gujarat"},

            {"name": "Bundi", "description": "Known for its stepwells and palaces, Bundi is a hidden architectural gem of Rajasthan.", "state": "Rajasthan"},
            {"name": "Bikaner", "description": "Famous for its camel breeding farm and unique desert culture.", "state": "Rajasthan"},
            {"name": "Kumbhalgarh", "description": "Home to the second-longest wall in the world and a majestic fort in the Aravallis.", "state": "Rajasthan"},

            {"name": "Kupwara", "description": "A scenic valley with pine forests and snow-capped mountains, less commercial than Gulmarg.", "state": "Jammu & Kashmir"},
            {"name": "Yusmarg", "description": "A peaceful meadow in Budgam district, great for trekking and picnics.", "state": "Jammu & Kashmir"},
            {"name": "Doodhpathri", "description": "A lesser-known grassland surrounded by deodar forests and flowing streams.", "state": "Jammu & Kashmir"},

            {"name": "Manas National Park", "description": "A UNESCO site less known than Kaziranga, rich in wildlife and scenic beauty.", "state": "Assam"},

            {"name": "Chilika Lake", "description": "Asia’s largest brackish water lagoon, home to migratory birds and dolphins.", "state": "Odisha"},

            {"name": "Yuksom", "description": "The base for treks to Dzongri and Goecha La, rich in monasteries and peaceful charm.", "state": "Sikkim"},

            {"name": "Mawlynnong", "description": "Dubbed Asia’s cleanest village, it's a hidden eco-tourism gem.", "state": "Meghalaya"},

            {"name": "Orchha", "description": "A historic town on the Betwa River, filled with palaces, temples, and quiet charm.", "state": "Madhya Pradesh"},
            {"name": "Pachmarhi", "description": "The only hill station in Madhya Pradesh, full of caves, waterfalls, and greenery.", "state": "Madhya Pradesh"},
            {"name": "Mandu", "description": "A fortified city with Afghan architecture, lakes, and romantic legends.", "state": "Madhya Pradesh"},

            {"name": "Jibhi", "description": "A quiet hamlet in the Tirthan Valley, Jibhi is known for its wooden cottages, lush greenery, and peaceful riverside vibe.", "state": "Himachal Pradesh"},
            {"name": "Barot Valley", "description": "A hidden gem for trekking and trout fishing, Barot offers stunning natural beauty away from tourist crowds.", "state": "Himachal Pradesh"},
            {"name": "Chitkul", "description": "The last inhabited village near the Indo-Tibet border, Chitkul is a serene destination with breathtaking mountain views.", "state": "Himachal Pradesh"},

            {"name": "Chitrakoot", "description": "A sacred site associated with Lord Rama, offering serene ghats and waterfalls.", "state": "Uttar Pradesh"},
            {"name": "Dudhwa National Park", "description": "A remote tiger reserve along the Indo-Nepal border with rich biodiversity.", "state": "Uttar Pradesh"},
            {"name": "Mahoba", "description": "Known for historic forts and stepwells, Mahoba is peaceful and culturally rich.", "state": "Uttar Pradesh"},

            {"name": "Bishnupur", "description": "Famous for terracotta temples and Baluchari sarees, it’s a cultural gem.", "state": "West Bengal"},
            {"name": "Jaldapara Wildlife Sanctuary", "description": "A forested area in north Bengal known for elephants and one-horned rhinos.", "state": "West Bengal"},
            {"name": "Taki", "description": "A serene riverside town near Bangladesh border ideal for weekend getaways.", "state": "West Bengal"},
            {"name": "Taki", "description": "A serene riverside town near Bangladesh border ideal for weekend getaways.", "state": "West Bengal"}
        ]

        place_objects = [Place(name=p["name"], description=p["description"], state=p["state"]) for p in places]
        db.session.add_all(place_objects)
        db.session.commit()

        images = [
                PlaceImage(place_id=place_objects[0].id, url="https://imgs.search.brave.com/ekMFTEOc3VDarFX1Dk7JYVeqX-8IqIKEY5ofEOP_qIs/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudG9paW1nLmNv/bS9waG90by9tc2lk/LTY4MDYyMzY2LHdp/ZHRoLTk2LGhlaWdo/dC02NS5jbXM"),
                PlaceImage(place_id=place_objects[1].id, url="https://imgs.search.brave.com/DrqRgv2mNmCIfztJrb1z_17QTPW5rk4o2PcaI-IdHqU/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9saDct/dXMuZ29vZ2xldXNl/cmNvbnRlbnQuY29t/L2RvY3N6L0FEXzRu/WGR0QzRLNjdZWVJj/am1jajlNb3pkZjV4/YnQ5OFNtcFZVeU9L/T3AwYUc1eEdCTjhB/Tld4TldERmZ0WTBk/MjJxOHl2bzlNT19p/YU9VWUNMVkE0SlZX/WG1lVGpDb2VLdVlV/TVpzeHhiSlRzR3JB/emRwR185Tlgwb2g0/WlFMVVF4ZERZVzk1/cDlSS202Uy1oZTlD/b3JCSGJxYUR6N0Q_/a2V5PXl0SzdKcmpG/ZkIxakEya3VnczlH/aGc"),
                PlaceImage(place_id=place_objects[2].id, url="https://imgs.search.brave.com/hLDH1jKIsGpYW8fsiOkik4O5wgSSijR7NODjnerZfPA/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly94cGxv/cmluZ2Rlc3RpbmF0/aW9ucy5jb20vd3At/Y29udGVudC91cGxv/YWRzLzIwMjMvMDcv/UG9jaGFyYW0tV2ls/ZGxpZmUtU2FuY3R1/YXJ5LVRpbWluZ3Mu/anBn"),
                PlaceImage(place_id=place_objects[3].id, url="https://images.hindustantimes.com/img/2022/11/06/1600x900/_098bfa70-ba9b-11e9-ab59-a9539248f706_1667733284898_1667733284898.png"),
                PlaceImage(place_id=place_objects[4].id, url="https://imgs.search.brave.com/_mm1_aAaGgYJYzmUj8LVXOmPZUVHSW7UM_IxKu_WmLw/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tb3Vu/dGFpbnZhbGxleS5p/bi9hc3NldHMvaW1h/Z2VzL21hcmVkdW1p/bGxpLXRvdXJpc20t/Z2FsbGVyeS0xMC05/MDB4NjAwLTgwMHg1/MzMuanBn"),
                PlaceImage(place_id=place_objects[5].id, url="https://imgs.search.brave.com/jc6lcXVN0b9zckjLbf0grvDMcx2zRxWPfx9MX4PYLsA/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90aGV3/YW5kZXJ0aGVyYXB5/LmNvbS93cC1jb250/ZW50L3VwbG9hZHMv/MjAyNC8wNC8yMy5n/YW5kaWtvdGEtZm9y/dC5qcGc"),
                PlaceImage(place_id=place_objects[6].id, url="https://imgs.search.brave.com/dTqYfCMu7CPQ7wn8wByOB-fjLDeo2onO6ezmTsSbU38/rs:fit:500:0:1:0/g:ce/aHR0cDovL3d3dy50/YXJrYXJsaS5pbmQu/aW4vaW1hZ2VzL3Rh/cmthcmxpLWJlYWNo/LTcuanBn"),
                PlaceImage(place_id=place_objects[7].id, url="https://imgs.search.brave.com/z1UF6rQL5Cz9KlWGA5UTPPnEMC1nh2LvqGQyjlaq3kI/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9oYmxp/bWcubW10Y2RuLmNv/bS9jb250ZW50L2h1/YmJsZS9pbWcvZGVz/dGdhbGxlcnlpbWFn/ZXMvbW10L2FjdGl2/aXRpZXMvbV9DaGlr/aGFsZGFyYV81X2xf/NTYzXzEwMDAuanBn"),
                PlaceImage(place_id=place_objects[8].id, url="https://imgs.search.brave.com/gaL38M7jgOIY1ek1vgQUKaFlnGTo3EqjZrrMOkawzwk/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tZWRp/YS1jZG4udHJpcGFk/dmlzb3IuY29tL21l/ZGlhL3Bob3RvLW8v/MDYvYTYvNTQvOTIv/YmhhbmRhcmRhcmEu/anBn"),
                PlaceImage(place_id=place_objects[9].id, url="https://imgs.search.brave.com/wsEUIfUDv48adufcMv8u0mawuZPEZ_C2OFsirB7PiNo/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90cmF2/ZWxzZXR1LmNvbS9h/cHBzL3VwbG9hZHMv/bmV3X2Rlc3RpbmF0/aW9uc19waG90b3Mv/ZGVzdGluYXRpb24v/MjAyMy8xMi8yMC82/MWE1YTA1YmZhYjQy/YzE1ZTM2M2M3MmY3/YjhiMzNiMF80MDB4/NDAwLnBuZw"),
                PlaceImage(place_id=place_objects[10].id, url="https://imgs.search.brave.com/OjHY4LHylUv2M5WXcAcsw-VuxAONiD_yQ7QSSdFmbEw/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly93d3cu/dHJhd2VsbC5pbi9h/ZG1pbi9pbWFnZXMv/dXBsb2FkLzE0NTk5/MjczM1phcndhbmlf/RmFsbC5qcGc"),
                PlaceImage(place_id=place_objects[11].id, url="https://imgs.search.brave.com/uREzpTooqkfFLiXez6t-DWhAJ5yuegpDteHsGuM6uM4/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9wb2xv/LWZvcmVzdC1sYW5k/c2NhcGUtaGlsbHMt/bGFrZS00Njk0Mjkx/Ni5qcGc"),
                PlaceImage(place_id=place_objects[12].id, url="https://imgs.search.brave.com/mwqnq_JfRUFANUwlZ4yTgYqEGdMIMPytKczRIMLFx7M/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly93d3cu/Y29ubW9jaGlsYS5j/b20vd3AtY29udGVu/dC91cGxvYWRzLzIw/MjMvMDgvODQzMDY2/MjQuanBn"),
                PlaceImage(place_id=place_objects[13].id, url="https://imgs.search.brave.com/dC2OXVSkLVn-8qwoq2zmplCfktlyXK9CShzs5I3AB-Q/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvNTM1/Mjc1Nzc0L3Bob3Rv/L2p1bmFnYXJoLWZv/cnQtaW4tYmlrYW5l/ci1yYWphc3RoYW4t/aW5kaWEuanBnP3M9/NjEyeDYxMiZ3PTAm/az0yMCZjPUw5TTdo/M3MxLVkwdWp2ai1E/Q3B1UjIzaVFWV2ZN/VE9GWnEzc2ctODUz/VGc9"),
                PlaceImage(place_id=place_objects[14].id, url="https://imgs.search.brave.com/8OJsVgnzcwDxB3dJ1JFUXJMLXYJdu_sG3CziU_deZzc/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9jZG4u/YXVkbGV5dHJhdmVs/LmNvbS83MDAvNDk5/Lzc5LzEwMTYxODkt/a3VtYmhhbGdhcmgt/cmFqYXN0aGFuLmpw/Zw"),
                PlaceImage(place_id=place_objects[15].id, url="https://imgs.search.brave.com/0SnTsreg3JDkoDsdj3AsuXK_D8KrHNv58c2_43Wjdrw/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzEwLzAxLzAxLzA2/LzM2MF9GXzEwMDEw/MTA2MDJfZGpVZjBX/ak45Nk5oc1JDeW5G/amhudVB5YXIyVGNi/clAuanBn"),
                PlaceImage(place_id=place_objects[16].id, url="https://imgs.search.brave.com/rJj8GraP-bgoYdk2xj5oRjnrAwyb5RCgyzG09x0iEj0/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly93d3cu/dG91cm15aW5kaWEu/Y29tL3N0YXRlcy9q/YW1tdS1rYXNobWly/L2ltYWdlL3l1c21h/cmctYmFubmVyLmpw/Zw"),
                PlaceImage(place_id=place_objects[17].id, url="https://imgs.search.brave.com/ZUC7bVdsk2gGYwraHnrKKL3edLOnL1RE2EU3chpbkZs/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vd3d3LnZp/YnJhbnRmb290c3Rl/cHMuY29tL3dwLWNv/bnRlbnQvdXBsb2Fk/cy8yMDIzLzA4L0RT/Q18zMjU1LVBTLXNj/YWxlZC5qcGc_cmVz/aXplPTEyMDAsNzEw/JnNzbD0x"),
                PlaceImage(place_id=place_objects[18].id, url="https://imgs.search.brave.com/j2VUmx5ERS8wz__jQgZWbEN4xrqMwZBQBONNH-egInw/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pbWcu/dHJhdmVsdHJpYW5n/bGUuY29tL2Jsb2cv/d3AtY29udGVudC91/cGxvYWRzLzIwMTgv/MDUvTU5QXzcwMHg0/NjYuanBn"),
                PlaceImage(place_id=place_objects[19].id, url="https://imgs.search.brave.com/98tYyuAts4n_iz9kREc1YWQMGmPY5GmXD_ptk5qq6EQ/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pbWli/aC5lZHUuaW4vaW1h/Z2VzL2dhbGxlcnkv/c21hbGxfaW1hZ2Vz/L2NoaWxpa2EtbGFr/ZS5wbmc"),
                PlaceImage(place_id=place_objects[20].id, url="https://imgs.search.brave.com/RxGML9t1QK4dIHRryy94FZtwdFKiDp5rtIpwQ39MIvg/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tZWRp/YS1jZG4udHJpcGFk/dmlzb3IuY29tL21l/ZGlhL3Bob3RvLW8v/MTEvNjAvZWYvOGEv/aW1nLTIwMTcxMTIy/LTA5MTUwMi1sYXJn/ZWpwZy5qcGc"),
                PlaceImage(place_id=place_objects[21].id, url="https://imgs.search.brave.com/eWa89xXByinFLVRqONNDoItdabcp9HQe0Mr_QE6hmJQ/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudG9paW1nLmNv/bS9waG90by9tc2lk/LTEwNjE1NDI3NCx3/aWR0aC05NixoZWln/aHQtNjUuY21z"),
                PlaceImage(place_id=place_objects[22].id, url="https://imgs.search.brave.com/Zy11uSF83KCpnlHV-S4V4WTHdSzOvZD8x6Y4UFQ9HYk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS1jZG4udHJpcGFk/dmlzb3IuY29tL21l/ZGlhL3Bob3RvLW8v/MDYvNjUvYTYvNGQv/b3JjaGhhLXdpbGRs/aWZlLXNhbmN0dWFy/eS5qcGc"),
                PlaceImage(place_id=place_objects[23].id, url="https://imgs.search.brave.com/mpOv2lhtCNc_4cK6ylJYh_seQyyse4YYZwQ0s0kmJlE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi93YXRl/cmZhbGwtYm9hdC1w/YWNobWFyaGktbWFk/aHlhLXByYWRlc2gt/Y2hhcm1pbmctdHJh/aWwtbmV0d29yay1t/b3VudGFpbi1zdXJy/b3VuZHMtbG9jYWwt/dmVuZG9ycy1vZmZl/cmluZy10ZWEtc25h/Y2tzLWp1bi0xNjAy/NjU0MDAuanBn"),
                PlaceImage(place_id=place_objects[24].id, url="https://imgs.search.brave.com/L2IKr4gdIa_H8B6ZPAis93NuizPW8zzh9PVSe5AbeF4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudG9paW1nLmNv/bS90aHVtYi83MTE4/NDA5Ny9NYW5kdS5q/cGc_d2lkdGg9NjM2/JmhlaWdodD0zNTgm/cmVzaXplPTQ"),
                PlaceImage(place_id=place_objects[25].id, url="https://imgs.search.brave.com/BCHluPd1NkwbXXSEubQz6pHDZpbhBVnrhgMTtfgho_w/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudG9paW1nLmNv/bS90aHVtYi9tc2lk/LTkzMDQ4MTg2LHdp/ZHRoLTc0OCxoZWln/aHQtNDk5LHJlc2l6/ZW1vZGU9NCxpbWdz/aXplLTIxMTcxMC9K/aWJoaS10aGUtcXVh/aW50LWdldGF3YXkt/aW4tSGltYWNoYWwt/UHJhZGVzaC5qcGc"),
                PlaceImage(place_id=place_objects[26].id, url="https://imgs.search.brave.com/WNl1cqpotL7eUDXalp_YxY6VYQyvEZebRboyQH9oh2k/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5zd2lwZXBhZ2Vz/LmNvbS8yMDIzLzQv/NjFlMDFjZDIyYzI3/MDEwMDEwM2ExNDBk/L2Rpc2NvdmVyaW5n/LXRoZS1oaWRkZW4t/Z2VtLW9mLWhpbWFj/aGFsLXByYWRlc2gt/LTUtLnBuZw"),
                PlaceImage(place_id=place_objects[27].id, url="https://imgs.search.brave.com/hGmtgWSPlSq18bPCWUuRqscy-qlWs7jlSX4ZCqGJlIU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMubGFuZ2ltZy5j/b20vdGh1bWIvOTE3/NDM4MDEvdHJla2tp/bmctaW4tY2hpdGt1/bC05MTc0MzgwMS5q/cGc_aW1nc2l6ZS0x/MzEzODAmd2lkdGg9/NjgwJnJlc2l6ZW1v/ZGU9Mw"),
                PlaceImage(place_id=place_objects[28].id, url="https://imgs.search.brave.com/Ey9A1jIFRKTk6gAmGhcWHmFteGEbnBnAxeaVWxOKS80/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/c2h1dHRlcnN0b2Nr/LmNvbS9pbWFnZS1w/aG90by9jaGl0cmFr/b290LW1hZGh5YS1w/cmFkZXNoLWluZGlh/LWphbnVhcnktMjYw/bnctMTQzMjQyODQx/My5qcGc"),
                PlaceImage(place_id=place_objects[29].id, url="https://imgs.search.brave.com/d9Ds568RAm_pwPl6NnjKdt_Qf9w87YFY0lff9B6e-GQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9hc3Nl/dHMudHJhdmVsdHJp/YW5nbGUuY29tL2Js/b2cvd3AtY29udGVu/dC91cGxvYWRzLzIw/MTcvMTIvQmVzdC1U/aW1lLVRvLVZpc2l0/LUR1ZGh3YS1OYXRp/b25hbC1QYXJrLmpw/Zw"),
                PlaceImage(place_id=place_objects[30].id, url="https://imgs.search.brave.com/LzDYfetD0gzuYDzVg-lr1euLIJ8K9xwD73KGfA6u2rc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jaGFs/b2dodW1hbmUuY29t/L3dwLWNvbnRlbnQv/dXBsb2Fkcy8yMDIx/LzA4L21haG9iYS10/b3VyLmpwZw"),
                PlaceImage(place_id=place_objects[31].id, url="https://imgs.search.brave.com/Yk942VdBf6tokifLPYwlaWnDgJbXVmZq5slDNp-go_A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9iZWF1/dGlmdWwtdmlldy1y/YXNtYW5jaGEtZmFt/b3VzLXRlcnJhY290/dGEtYW5jaWVudC10/ZW1wbGUtYmlzaG51/cHVyLXdlc3QtYmVu/Z2FsLWluZGlhLXJh/c21hbmNoYS0xOTI3/MjcwNDkuanBn"),
                PlaceImage(place_id=place_objects[32].id, url="https://imgs.search.brave.com/1KfL78zohcxPfh9G2Xvxuzs69yWjSyTDmvcUDcYohsc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/YnJpdGFubmljYS5j/b20vNzIvMTQyNTcy/LTAwNC0wRkQ1MjRD/NS9lbGVwaGFudC1z/YWZhcmktSmFsZGFw/YXJhLVdpbGRsaWZl/LVNhbmN0dWFyeS1J/bmRpYS1XZXN0Lmpw/Zw"),
                PlaceImage(place_id=place_objects[33].id, url="https://imgs.search.brave.com/_OM98QOnAxXkyAfxaZsHpyJxSAcLs2sEnwI82kKHZ6E/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly91cGxv/YWQud2lraW1lZGlh/Lm9yZy93aWtpcGVk/aWEvY29tbW9ucy8z/LzM5L1Rha2lfVmll/d0Zyb21HdWVzdEhv/dXNlLmpwZw"),
            ]

        db.session.add_all(images)
        db.session.commit()

if __name__ == "__main__":

    chatbot_path = os.path.join(os.path.dirname(__file__), 'chatbot', 'app.py')

    # Run Streamlit chatbot in background
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", chatbot_path,
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    with app.app_context():
        db.create_all()
        insert_places()
    app.run(debug=True , use_reloader=False)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
