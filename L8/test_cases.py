# Development set: 10 test cases with ideal answers
# Each test case has a customer_message and the expected ideal_answer

dev_set = [
    {
        "customer_message": "Which TV can I buy if I'm on a budget?",
        "ideal_answer": {
            "Televisions and Home Theater Systems": {
                "CineView 4K TV",
                "SoundMax Home Theater",
                "CineView 8K TV",
                "SoundMax Soundbar",
                "CineView OLED TV",
            }
        },
    },
    {
        "customer_message": "I need a charger for my smartphone",
        "ideal_answer": {
            "Smartphones and Accessories": {
                "MobiTech PowerCase",
                "MobiTech Wireless Charger",
            }
        },
    },
    {
        "customer_message": "What computers do you have?",
        "ideal_answer": {
            "Computers and Laptops": {
                "TechPro Ultrabook",
                "BlueWave Gaming Laptop",
                "PowerLite Convertible",
                "TechPro Desktop",
                "BlueWave Chromebook",
            }
        },
    },
    {
        "customer_message": "Tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what TVs do you have?",
        "ideal_answer": {
            "Smartphones and Accessories": {"SmartX ProPhone"},
            "Cameras and Camcorders": {"FotoSnap DSLR Camera"},
            "Televisions and Home Theater Systems": {
                "CineView 4K TV",
                "SoundMax Home Theater",
                "CineView 8K TV",
                "SoundMax Soundbar",
                "CineView OLED TV",
            },
        },
    },
    {
        "customer_message": "tell me about the CineView TV, the 8K one, Gamesphere console, the X one. I'm on a budget, what computers do you have?",
        "ideal_answer": {
            "Televisions and Home Theater Systems": {"CineView 8K TV"},
            "Gaming Consoles and Accessories": {"GameSphere X"},
            "Computers and Laptops": {
                "TechPro Ultrabook",
                "BlueWave Gaming Laptop",
                "PowerLite Convertible",
                "TechPro Desktop",
                "BlueWave Chromebook",
            },
        },
    },
    {
        "customer_message": "What smartphones do you have?",
        "ideal_answer": {
            "Smartphones and Accessories": {
                "SmartX ProPhone",
                "MobiTech PowerCase",
                "SmartX MiniPhone",
                "MobiTech Wireless Charger",
                "SmartX EarBuds",
            }
        },
    },
    {
        "customer_message": "I'm looking for headphones. What options do you have?",
        "ideal_answer": {
            "Audio Equipment": {
                "AudioPhonic Noise-Canceling Headphones",
                "WaveSound Bluetooth Speaker",
                "AudioPhonic True Wireless Earbuds",
                "WaveSound Soundbar",
                "AudioPhonic Turntable",
            }
        },
    },
    {
        "customer_message": "What do you know about the GameSphere Y gaming console? Also, I'd like info on the AudioPhonic noise-canceling headphones.",
        "ideal_answer": {
            "Gaming Consoles and Accessories": {"GameSphere Y"},
            "Audio Equipment": {"AudioPhonic Noise-Canceling Headphones"},
        },
    },
    {
        "customer_message": "I'd like to compare the FotoSnap DSLR Camera with the FotoSnap Mirrorless Camera",
        "ideal_answer": {
            "Cameras and Camcorders": {
                "FotoSnap DSLR Camera",
                "FotoSnap Mirrorless Camera",
            }
        },
    },
    {
        "customer_message": "I would like hot tub time machine",
        "ideal_answer": {},
    },
]
