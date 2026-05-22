DIALOGUES = {

    "Tavern Keeper": {

        "talk": [
            {
                "texts": [
                    "Quiet tonight...",
                    "Not many travelers today."
                ],
                "required_tags": ["tavern", "evening"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Late nights are exhausting.",
                    "I should close earlier."
                ],
                "required_tags": ["tavern", "night"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Rain scares travelers away.",
                    "Wet boots, empty purses. Bad weather for business."
                ],
                "required_tags": ["tavern", "rain"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "War makes every cup taste bitter.",
                    "People whisper more when soldiers are near."
                ],
                "required_tags": ["tavern", "war"],
                "forbidden_tags": ["combat"]
            }
        ],

        "reply": [
            {
                "texts": [
                    "Indeed.",
                    "Could be worse."
                ],
                "required_tags": ["reply", "tavern"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Keep your voice down.",
                    "Walls listen better at night."
                ],
                "required_tags": ["reply", "tavern", "night"],
                "forbidden_tags": ["combat"]
            }
        ]
    },

    "Knight": {

        "talk": [
            {
                "texts": [
                    "I do not like quiet rooms.",
                    "A tavern is safest before everyone starts shouting."
                ],
                "required_tags": ["tavern"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "At night, even old armor sounds nervous.",
                    "I will take the door watch tonight."
                ],
                "required_tags": ["tavern", "night"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Rain covers tracks too well.",
                    "Bad weather makes bad news travel slower."
                ],
                "required_tags": ["rain"],
                "forbidden_tags": ["combat"]
            },

            {
                "texts": [
                    "It's nice to walk in the forest when it's not raining.",
                    "The forest is peaceful when the weather is good."
                ],
                "required_tags": ["goal_walk_in_forest"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "I should rest at the tavern now.",
                    "Time to head back to the tavern for some rest."
                ],
                "required_tags": ["goal_rest"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "I need to walk in the forest now.",
                    "I should head to the forest now.",
                    "I have some business to take care of in the forest."
                ],
                "required_tags": ["moving_to_forest"],
                "forbidden_tags": ["combat"]
            },
                {
                    "texts": [
                        "I should rest now.",
                        "I need to head back to the tavern for some rest.",
                        "I have been walking in the forest for a while, it's time to rest."
                    ],
                    "required_tags": ["moving_to_tavern"],
                    "forbidden_tags": ["combat"]
                }

        ],

        "reply": [
            {
                "texts": [
                    "That sounds right.",
                    "I have seen worse signs."
                ],
                "required_tags": ["reply"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "War talk belongs outside, not beside the hearth.",
                    "Then we should count food, blades, and exits."
                ],
                "required_tags": ["reply", "war"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "You always say that after midnight.",
                    "Then close before trouble finds us."
                ],
                "required_tags": ["reply", "speaker_tavern_keeper", "night"],
                "forbidden_tags": ["combat"]
            }
        ]
    },

    "Squire": {

        "talk": [
            {
                "texts": [
                    "I could eat a whole loaf.",
                    "Does anyone else smell stew?"
                ],
                "required_tags": ["tavern"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Morning makes this place look almost respectable.",
                    "I thought taverns were quieter in the morning."
                ],
                "required_tags": ["tavern", "morning"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Afternoon is the best time for gossip.",
                    "I like to listen to the stories in the afternoon."
                ],
                "required_tags": ["tavern", "afternoon"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Evening is when the real fun starts!",
                    "I hope we get to stay up late tonight!"
                ],
                "required_tags": ["tavern", "evening"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "The rain sounds like fingers on the shutters.",
                    "I hope the road is not mud by dawn."
                ],
                "required_tags": ["rain"],
                "forbidden_tags": ["combat"]
            }
        ],

        "reply": [
            {
                "texts": [
                    "If you say so.",
                    "I had not thought of that."
                ],
                "required_tags": ["reply"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "I can check the horses.",
                    "Should I bar the door?"
                ],
                "required_tags": ["reply", "night"],
                "forbidden_tags": ["combat"]
            },
            {
                "texts": [
                    "Yes, sir.",
                    "I will keep my eyes open."
                ],
                "required_tags": ["reply", "speaker_knight"],
                "forbidden_tags": ["combat"]
            }
        ]
    }
}
