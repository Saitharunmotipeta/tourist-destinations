from app import app
from extensions import db
from models import Place, PlaceImage

def insert_places():
    with app.app_context():
        # Optional: Clear existing entries
        db.session.query(PlaceImage).delete()
        db.session.query(Place).delete()
        db.session.commit()

        # Define places with descriptions and states
        places = [
            # Telangana
            {"name": "Charminar", "description": "An iconic landmark in Hyderabad, Charminar is known for its architectural brilliance and vibrant markets surrounding it.", "state": "Telangana"},
            {"name": "Golconda Fort", "description": "A majestic fort showcasing rich history and panoramic views of Hyderabad.", "state": "Telangana"},
            {"name": "Ramoji Film City", "description": "A sprawling film studio complex and tourist hub offering guided tours and fun activities.", "state": "Telangana"},

            # Andhra Pradesh
            {"name": "Tirupati", "description": "Home to the famous Tirumala Venkateswara Temple, Tirupati is a major pilgrimage site.", "state": "Andhra Pradesh"},
            {"name": "Araku Valley", "description": "A scenic hill station known for lush coffee plantations and pleasant weather.", "state": "Andhra Pradesh"},
            {"name": "Vishakhapatnam", "description": "A coastal city offering pristine beaches, temples, and scenic beauty.", "state": "Andhra Pradesh"},

            # Maharashtra
            {"name": "Mumbai", "description": "The bustling metropolis of Mumbai offers iconic attractions like the Gateway of India and Marine Drive.", "state": "Maharashtra"},
            {"name": "Aurangabad", "description": "Aurangabad is home to the magnificent Ajanta and Ellora Caves, showcasing ancient art and architecture.", "state": "Maharashtra"},
            {"name": "Mahabaleshwar", "description": "A serene hill station, Mahabaleshwar offers stunning views, strawberries, and pleasant weather.", "state": "Maharashtra"},

            # Gujarat
            {"name": "Statue of Unity", "description": "The world's tallest statue, located near the Sardar Sarovar Dam, honors Sardar Vallabhbhai Patel.", "state": "Gujarat"},
            {"name": "Gir National Park", "description": "The last abode of Asiatic lions, Gir is a wildlife enthusiast's paradise.", "state": "Gujarat"},
            {"name": "Rann of Kutch", "description": "A vast salt marsh that transforms into a cultural extravaganza during the Rann Utsav.", "state": "Gujarat"},

            # Rajasthan
            {"name": "Jaipur", "description": "Known as the 'Pink City', Jaipur offers historic palaces, vibrant markets, and cultural experiences.", "state": "Rajasthan"},
            {"name": "Udaipur", "description": "The 'City of Lakes', Udaipur is famed for its picturesque lakes and grand palaces.", "state": "Rajasthan"},
            {"name": "Jaisalmer", "description": "The 'Golden City', Jaisalmer is renowned for its fort, desert safaris, and intricate architecture.", "state": "Rajasthan"},

            # Jammu & Kashmir
            {"name": "Srinagar", "description": "Known for its Dal Lake, houseboats, and scenic gardens, Srinagar is a paradise on earth.", "state": "Jammu & Kashmir"},
            {"name": "Gulmarg", "description": "A popular ski destination offering breathtaking views of snow-covered peaks.", "state": "Jammu & Kashmir"},
            {"name": "Pahalgam", "description": "A serene town surrounded by lush meadows and rivers, ideal for nature lovers.", "state": "Jammu & Kashmir"},

            # Eastern States
            {"name": "Kaziranga National Park", "description": "Home to the one-horned rhinoceros, this UNESCO site is a wildlife haven in Assam.", "state": "Assam"},
            {"name": "Konark Sun Temple", "description": "A UNESCO World Heritage site in Odisha, known for its intricate architecture.", "state": "Odisha"},
            {"name": "Gangtok", "description": "The capital of Sikkim offers stunning views of the Kanchenjunga and serene monasteries.", "state": "Sikkim"},
            {"name": "Shillong", "description": "Known as the 'Scotland of the East', Shillong boasts waterfalls and lush landscapes.", "state": "Meghalaya"},

            # Madhya Pradesh
            {"name": "Khajuraho Temples", "description": "A UNESCO site known for its exquisite sculptures and rich history.", "state": "Madhya Pradesh"},
            {"name": "Bandhavgarh National Park", "description": "A prime destination for tiger safaris and wildlife enthusiasts.", "state": "Madhya Pradesh"},
            {"name": "Sanchi Stupa", "description": "A Buddhist site showcasing ancient art and architecture.", "state": "Madhya Pradesh"},

            # Delhi
            {"name": "India Gate", "description": "A historic war memorial surrounded by lush gardens, perfect for an evening stroll.", "state": "Delhi"},
            {"name": "Red Fort", "description": "A UNESCO site symbolizing India's history and heritage.", "state": "Delhi"},
            {"name": "Qutub Minar", "description": "The world's tallest brick minaret and a UNESCO World Heritage site.", "state": "Delhi"},

            # Uttar Pradesh
            {"name": "Taj Mahal", "description": "A symbol of love and a UNESCO site, the Taj Mahal is an architectural marvel.", "state": "Uttar Pradesh"},
            {"name": "Varanasi", "description": "The spiritual capital of India, known for its ghats and vibrant culture.", "state": "Uttar Pradesh"},
            {"name": "Lucknow", "description": "Known for its Nawabi heritage, exquisite cuisine, and historical sites.", "state": "Uttar Pradesh"},

            # West Bengal
            {"name": "Kolkata", "description": "The 'City of Joy' offers colonial architecture, vibrant culture, and delicious cuisine.", "state": "West Bengal"},
            {"name": "Darjeeling", "description": "Known for its tea gardens and stunning views of the Himalayas.", "state": "West Bengal"},
            {"name": "Sundarbans", "description": "A UNESCO site, home to the Bengal tiger and rich biodiversity.", "state": "West Bengal"},
        ]

        # Insert places into the database
        place_objects = []
        for place in places:
            place_objects.append(Place(name=place["name"], description=place["description"], state=place["state"]))
        
        db.session.add_all(place_objects)
        db.session.commit()

        images = [
                PlaceImage(place_id=place_objects[0].id, url="https://imgs.search.brave.com/xFWuoTnhfIQOlzBU3FrNK52G4cRdXhe3q1Uf_2ZoDLA/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9jaGFy/bWluYXItbmlnaHQt/ZWlkLXZpYnJhbnQt/Y29sb3JzLWFsbC1h/cm91bmQtMTU3OTAz/NzM4LmpwZw"),
                PlaceImage(place_id=place_objects[1].id, url="https://www.therevolverclub.com/cdn/shop/articles/image_2022-05-25_221257668.png?v=1687777245&width=1200"),
                PlaceImage(place_id=place_objects[2].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRr9_eGSmm6ig1N_I6XxJk7idLQ5EfJkev4AQ&s"),
                PlaceImage(place_id=place_objects[3].id, url="https://images.hindustantimes.com/img/2022/11/06/1600x900/_098bfa70-ba9b-11e9-ab59-a9539248f706_1667733284898_1667733284898.png"),
                PlaceImage(place_id=place_objects[4].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhFDunX20khWOZIGDrkqBlUauD0SKSO8HmwQ&s"),
                PlaceImage(place_id=place_objects[5].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSC6csp5db_-r1jh4WoRy07r6X2vtqRto9SA&s"),
                PlaceImage(place_id=place_objects[6].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMkOoZtJ2sv48M5Z30ZehKAQFiUI_1XPAMaA&s"),
                PlaceImage(place_id=place_objects[7].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlSXwFnk4SOYjFzGGvJSCZkSSJig8_ej4lEw&s"),
                PlaceImage(place_id=place_objects[8].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQv268ucqb3KK94vWFkkTGVeAEbGolxDFQFlw&s"),
                PlaceImage(place_id=place_objects[9].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTzcNX1RocA7gmHq1oEcZNp-e-kgR-Wwi_Kw&s"),
                PlaceImage(place_id=place_objects[10].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJ8zI6FJFHp_DrkOVPqmEvmOYXgHez-IlBJw&s"),
                PlaceImage(place_id=place_objects[11].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtChxV9drUaQmBMbo9g4cOLete-AvUbPWX2A&s"),
                PlaceImage(place_id=place_objects[12].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ83g0EeMwNKcLxsGBhYGHzJFd-scr36WD0nw&s"),
                PlaceImage(place_id=place_objects[13].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSInd3SMuxvC_mP7KNzR1uhqfsEuZ0phDPs4Q&s"),
                PlaceImage(place_id=place_objects[14].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgFutd-W8jFLMTQqJRie7DHm8br32pw8RfXg&s"),
                PlaceImage(place_id=place_objects[15].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrIZDF6ubwPdnbTzyeSB6IsOTeGSFP1lrfkQ&s"),
                PlaceImage(place_id=place_objects[16].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbtAkos8-dMNG6rFvNlUT_cdZJ1BubA9n6sg&s"),
                PlaceImage(place_id=place_objects[17].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsD4EZZW2_jEsa43bmo3Zv-EezLaq1YUfWAw&s"),
                PlaceImage(place_id=place_objects[18].id, url="https://upload.wikimedia.org/wikipedia/commons/5/51/Khajuraho_Group_of_Monuments.jpg"),
                PlaceImage(place_id=place_objects[19].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAcM70I1Uyg2uUnAa36_eis9EUMYHSXAqbBg&s"),
                PlaceImage(place_id=place_objects[20].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyNVuvbfsw4OXW6hchqeN8CEpUbVkXsnylsA&s"),
                PlaceImage(place_id=place_objects[21].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2q20qEv-jh9KuXReBFz0RCFu8WvrAyT-7vw&s"),
                PlaceImage(place_id=place_objects[22].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGwxpAxw7rINlT9r833JIIx2cyssUsyjn8ZA&s"),
                PlaceImage(place_id=place_objects[23].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8vuwMC09NpVqQKevry9PnjZcIcVUHUJApGQ&s"),
                PlaceImage(place_id=place_objects[24].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThEVguzPcmw3nKsS9lAt_gr3_Cwd2qFfT_GQ&s"),
                PlaceImage(place_id=place_objects[25].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeSqZx6OOqgN1wWag3XdrZMnsyl_1KwH8yLg&s"),
                PlaceImage(place_id=place_objects[26].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS76II8j8JICzPg6F_8h8RqYAFsZQEKxJcq0Q&s"),
                PlaceImage(place_id=place_objects[27].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCzt_0rJWwK__3apZ8NEwV_BnHWI8bN5r-qg&s"),
                PlaceImage(place_id=place_objects[28].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKziiWBsB4NJlFnPdQT3YsnZXOhi-sDHHIlw&s"),
                PlaceImage(place_id=place_objects[29].id, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbsp_hmG-BLUpDC2bhaiDbQlszntaNOnvb-Q&s"),
            ]


        db.session.add_all(images)
        db.session.commit()

        print("✅ Places and images inserted successfully.")

if __name__ == "__main__":
    insert_places()
