# -*- coding: utf-8 -*-
"""
BFDI Episode List - EDIT THIS FILE TO CUSTOMIZE WHAT GETS SCRAPED

Each episode has:
- title: The episode name (used to build the transcript URL)
- number: Episode number in the series
- season: Which season/series it belongs to

TO REMOVE AN EPISODE: Just delete or comment out that line
TO ADD AN EPISODE: Add a new dict with title, number, season

The transcript URL is built as:
https://battlefordreamisland.fandom.com/wiki/{title}/Transcript
(spaces become underscores, special chars get URL-encoded)
"""

EPISODES = [
    # ==================== SEASON 1: Battle for Dream Island ====================
    {"title": "Take the Plunge: Part 1", "number": 1, "season": 1, "season_name": "BFDI"},
    {"title": "Take the Plunge: Part 2", "number": 2, "season": 1, "season_name": "BFDI"},
    {"title": "Barriers and Pitfalls", "number": 3, "season": 1, "season_name": "BFDI"},
    {"title": "Are You Smarter Than a Snowball?", "number": 4, "season": 1, "season_name": "BFDI"},
    {"title": "Sweet Tooth", "number": 5, "season": 1, "season_name": "BFDI"},
    {"title": "Bridge Crossing", "number": 6, "season": 1, "season_name": "BFDI"},
    {"title": "Power of Three", "number": 7, "season": 1, "season_name": "BFDI"},
    {"title": "Puzzling Mysteries", "number": 8, "season": 1, "season_name": "BFDI"},
    {"title": "Cycle of Life", "number": 9, "season": 1, "season_name": "BFDI"},
    {"title": "Insectophobe's Nightmare", "number": 10, "season": 1, "season_name": "BFDI"},
    {"title": "Crybaby!", "number": 11, "season": 1, "season_name": "BFDI"},
    {"title": "Lofty", "number": 12, "season": 1, "season_name": "BFDI"},
    {"title": "A Leg Up in the Race", "number": 13, "season": 1, "season_name": "BFDI"},
    {"title": "Don't Lose Your Marbles", "number": 14, "season": 1, "season_name": "BFDI"},
    {"title": "Half a Loaf Is Better Than None", "number": 15, "season": 1, "season_name": "BFDI"},
    {"title": "Vomitaco", "number": 16, "season": 1, "season_name": "BFDI"},
    {"title": "Bowling, Now with Explosions!", "number": 17, "season": 1, "season_name": "BFDI"},
    {"title": "The Reveal", "number": 18, "season": 1, "season_name": "BFDI"},
    {"title": "Reveal Novum", "number": 19, "season": 1, "season_name": "BFDI"},
    {"title": "Rescission", "number": 20, "season": 1, "season_name": "BFDI"},
    {"title": "Gardening Hero", "number": 21, "season": 1, "season_name": "BFDI"},
    {"title": "The Glistening", "number": 22, "season": 1, "season_name": "BFDI"},
    {"title": "Don't Pierce My Flesh", "number": 23, "season": 1, "season_name": "BFDI"},
    {"title": "Hurtful!", "number": 24, "season": 1, "season_name": "BFDI"},
    {"title": "Insectophobe's Nightmare 2", "number": 25, "season": 1, "season_name": "BFDI"},
    {"title": "Return of the Hang Glider", "number": 26, "season": 1, "season_name": "BFDI"},

    # ==================== SEASON 2: Battle for Dream Island Again ====================
    {"title": "Yeah, Who? I Wanna Know", "number": 27, "season": 2, "season_name": "BFDIA"},
    {"title": "Get Digging", "number": 28, "season": 2, "season_name": "BFDIA"},
    {"title": "Insectophobe's Nightmare 3", "number": 29, "season": 2, "season_name": "BFDIA"},
    {"title": "Zeeky Boogy Doog", "number": 30, "season": 2, "season_name": "BFDIA"},
    {"title": "Get in the Van", "number": 31, "season": 2, "season_name": "BFDIA"},
    {"title": "No More Snow!", "number": 33, "season": 2, "season_name": "BFDIA"},
    {"title": "It's a Monster", "number": 34, "season": 2, "season_name": "BFDIA"},
    {"title": "The Long-lost Yoyle City", "number": 35, "season": 2, "season_name": "BFDIA"},
    {"title": "Well Rested", "number": 36, "season": 2, "season_name": "BFDIA"},
    {"title": "Intruder Alert", "number": 37, "season": 2, "season_name": "BFDIA"},
    {"title": "Meaty", "number": 38, "season": 2, "season_name": "BFDIA"},
    {"title": "Catch These Hands", "number": 39, "season": 2, "season_name": "BFDIA"},
    {"title": "Taste the Sweetness", "number": 40, "season": 2, "season_name": "BFDIA"},
    {"title": "Lots of Mud", "number": 41, "season": 2, "season_name": "BFDIA"},
    {"title": "Insectophobe's Nightmare 4", "number": 42, "season": 2, "season_name": "BFDIA"},
    {"title": "Well, Look Who It Is!", "number": 43, "season": 2, "season_name": "BFDIA"},
    {"title": "PointyPointyPointy ♫", "number": 44, "season": 2, "season_name": "BFDIA"},
    {"title": "Spore Day", "number": 45, "season": 2, "season_name": "BFDIA"},
    {"title": "Respect to the Wicked", "number": 46, "season": 2, "season_name": "BFDIA"},
    {"title": "Start the Shift", "number": 47, "season": 2, "season_name": "BFDIA"},
    {"title": "Airplanes in the Night Sky", "number": 48, "season": 2, "season_name": "BFDIA"},
    {"title": "🥚", "number": 49, "season": 2, "season_name": "BFDIA"},
    {"title": "Launch Party", "number": 50, "season": 2, "season_name": "BFDIA"},
    {"title": "We're Not Friends", "number": 51, "season": 2, "season_name": "BFDIA"},
    {"title": "I'm the Main Character", "number": 52, "season": 2, "season_name": "BFDIA"},
    {"title": "Shattered!", "number": 53, "season": 2, "season_name": "BFDIA"},

    # ==================== SEASON 3: IDFB ====================
    {"title": "Welcome Back", "number": 54, "season": 3, "season_name": "IDFB"},

    # ==================== SEASON 4: Battle for BFDI / Battle for BFB ====================
    {"title": "Getting Teardrop to Talk", "number": 55, "season": 4, "season_name": "BFB"},
    {"title": "Lick Your Way to Freedom", "number": 56, "season": 4, "season_name": "BFB"},
    {"title": "Why Would You Do This on a Swingset", "number": 57, "season": 4, "season_name": "BFB"},
    {"title": "Today's Very Special Episode", "number": 58, "season": 4, "season_name": "BFB"},
    {"title": "Fortunate Ben", "number": 59, "season": 4, "season_name": "BFB"},
    {"title": "Four Goes Too Far", "number": 60, "season": 4, "season_name": "BFB"},
    {"title": "The Liar Ball You Don't Want", "number": 61, "season": 4, "season_name": "BFB"},
    {"title": "Questions Answered", "number": 62, "season": 4, "season_name": "BFB"},
    {"title": "This Episode Is About Basketball", "number": 63, "season": 4, "season_name": "BFB"},
    {"title": "Enter the Exit", "number": 64, "season": 4, "season_name": "BFB"},
    {"title": "Get to the Top in 500 Steps", "number": 65, "season": 4, "season_name": "BFB"},
    {"title": "What Do You Think of Roleplay?", "number": 66, "season": 4, "season_name": "BFB"},
    {"title": "Return of the Rocket Ship", "number": 67, "season": 4, "season_name": "BFB"},
    {"title": "Don't Dig Straight Down", "number": 68, "season": 4, "season_name": "BFB"},
    {"title": "The Four is Lava", "number": 69, "season": 4, "season_name": "BFB"},
    {"title": "The Escape from Four", "number": 70, "season": 4, "season_name": "BFB"},
    {"title": "X Marks the Spot", "number": 71, "season": 4, "season_name": "BFB"},
    {"title": "Take the Tower", "number": 72, "season": 4, "season_name": "BFB"},
    {"title": "How Loe Can You Grow?", "number": 73, "season": 4, "season_name": "BFB"},
    {"title": "A Taste of Space", "number": 74, "season": 4, "season_name": "BFB"},
    {"title": "Let's Raid The Warehouse", "number": 75, "season": 4, "season_name": "BFB"},
    {"title": "Who Stole Donut's Diary?", "number": 76, "season": 4, "season_name": "BFB"},
    {"title": "Fashion For Your Face!", "number": 77, "season": 4, "season_name": "BFB"},
    {"title": "The Game Has Changed", "number": 78, "season": 4, "season_name": "BFB"},
    {"title": "The Tweested Temple", "number": 79, "season": 4, "season_name": "BFB"},
    {"title": "The Hidden Contestant", "number": 80, "season": 4, "season_name": "BFB"},
    {"title": "Uprooting Everything", "number": 81, "season": 4, "season_name": "BFB"},
    {"title": "B.F.B. = Back From Beginning", "number": 82, "season": 4, "season_name": "BFB"},
    {"title": "SOS (Save Our Show)", "number": 83, "season": 4, "season_name": "BFB"},
    {"title": "Chapter Complete", "number": 84, "season": 4, "season_name": "BFB"},

    # ==================== SEASON 5: The Power of Two ====================
    {"title": "You Know Those Buttons Don't Do Anything, Right?", "number": 80, "season": 5, "season_name": "TPOT"},
    {"title": "The Worst Day of Black Hole's Life", "number": 81, "season": 5, "season_name": "TPOT"},
    {"title": "Getting Puffball To Think About Rollercoasters", "number": 82, "season": 5, "season_name": "TPOT"},
    {"title": "Gardening Zero", "number": 83, "season": 5, "season_name": "TPOT"},
    {"title": "Fishes and Dishes", "number": 84, "season": 5, "season_name": "TPOT"},
    {"title": "The Great Goikian Bake-Off", "number": 85, "season": 5, "season_name": "TPOT"},
    {"title": "The Seven Wonders of Goiky", "number": 86, "season": 5, "season_name": "TPOT"},
    {"title": "Balancing P.A.C.T.", "number": 87, "season": 5, "season_name": "TPOT"},
    {"title": "Outbreak At Stake", "number": 88, "season": 5, "season_name": "TPOT"},
    {"title": "Oneirophobe's Nightmare", "number": 89, "season": 5, "season_name": "TPOT"},
    {"title": "Out Of The Blue", "number": 90, "season": 5, "season_name": "TPOT"},
    {"title": "What's Up Bell's String?", "number": 91, "season": 5, "season_name": "TPOT"},
    {"title": "Category One", "number": 92, "season": 5, "season_name": "TPOT"},
    {"title": "I SAID CAREFUL!!", "number": 93, "season": 5, "season_name": "TPOT"},
    {"title": "Seasonal Shift", "number": 94, "season": 5, "season_name": "TPOT"},
    {"title": "The Power Of Four", "number": 95, "season": 5, "season_name": "TPOT"},
    {"title": "Bottle For Dream Island", "number": 96, "season": 5, "season_name": "TPOT"},
    {"title": "BFB 31", "number": 97, "season": 5, "season_name": "TPOT"},
    {"title": "Last One Standing", "number": 98, "season": 5, "season_name": "TPOT"},
    {"title": "Alone", "number": 99, "season": 5, "season_name": "TPOT"},
]


# Quick stats
if __name__ == "__main__":
    print(f"Total episodes: {len(EPISODES)}")
    for season in range(1, 6):
        count = len([e for e in EPISODES if e["season"] == season])
        print(f"Season {season}: {count} episodes")
