#!/usr/bin/env python3
"""
Article Updater for Daudi's Blog
This script adds the new "Two Flights, Two Philosophies" article to the blog data.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

class ArticleUpdater:
    """
    Manages adding and updating articles in a JSON file.
    """
    def __init__(self, articles_file: str = 'data/articles.json'):
        self.articles_file = articles_file
        # Ensure the directory exists before loading
        os.makedirs(os.path.dirname(self.articles_file), exist_ok=True)
        self.articles_data = self.load_articles()
    
    def load_articles(self) -> Dict[str, Any]:
        """Load articles from JSON file"""
        try:
            with open(self.articles_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create the file with an empty list if it doesn't exist
            with open(self.articles_file, 'w', encoding='utf-8') as f:
                initial_data = {"articles": []}
                json.dump(initial_data, f, indent=2)
            return {"articles": []}
    
    def save_articles(self) -> None:
        """Save articles back to JSON file"""
        with open(self.articles_file, 'w', encoding='utf-8') as f:
            json.dump(self.articles_data, f, indent=2)
    
    def add_article(self, article: Dict[str, Any]) -> None:
        """Add a new article, checking for duplicates by ID."""
        required_fields = ['id', 'title', 'category', 'content']
        for field in required_fields:
            if field not in article:
                raise ValueError(f"Missing required field: {field}")

        # Check if an article with this ID already exists
        if any(a['id'] == article['id'] for a in self.articles_data['articles']):
            print(f"Article with ID '{article['id']}' already exists. Skipping.")
            return

        if 'date' not in article:
            article['date'] = datetime.now().strftime('%B %d, %Y')
        
        if 'image' not in article:
            article['image'] = f"{article['id']}.jpg"
        
        self.articles_data['articles'].append(article)
        self.save_articles()
        print(f"Added article: {article['title']}")
    
    def list_articles(self) -> None:
        """List all articles"""
        print("\nCurrent Articles:")
        print("-" * 50)
        if not self.articles_data['articles']:
            print("No articles found.")
            return
        for i, article in enumerate(self.articles_data['articles'], 1):
            print(f"{i}. {article['title']} ({article['category']}) - {article['date']}")

def get_flight_article_data() -> Dict[str, Any]:
    """
    Contains the data for the 'Two Flights, Two Philosophies' article.
    """
    title = "Two Flights, Two Philosophies: From the A350 to the 737 MAX"
    # Content is split into paragraphs (strings in a list)
    content = [
        "There are moments when your life's passions—engineering, aviation, technology—don't just converge, they collide. My journey today from Lagos was one of those collisions. I was about to fly on two of the most talked-about aircraft in the world, machines that tell two profoundly different stories about humanity's relationship with the sky.",
        "First, the Airbus A350-1000, a vision of the future. Then, the Boeing 737 MAX, a legend grappling with its own legacy. This isn't just a trip report; it's a tale of two philosophies, and I had a front-row seat.",
        "### The Soul of a New Machine: The A350 from Seat 36L",
        "The experience began before I even stepped on board. Standing at the pre-boarding area for Gate E55 at Murtala Muhammed International, I knew this would be interesting. E55 is tucked away in a tight corner of the terminal, a gate that requires a sharp, almost delicate turn for any aircraft, let alone one of the largest passenger jets in the sky. I watched her approach, ET-BAX, an A350-1000. She was immense, yet moved with an impossible grace. The nose wheel swiveled at an angle so sharp it defied belief, a beautiful, exaggerated display of agility as she navigated the confined space before a tow tractor gently nudged her into place. This was no mere airplane; this was a statement.",
        "Boarding in Zone 3, I made my way to 36L and braced for the usual compromise of a 6'2\" frame in an economy seat. I sat down and my brain stopped. My knees had space. A lot of space. Nearly half a foot of it. I looked out the window and realized my seat was perfectly aligned with the wing's centerline, and a quick glance down confirmed the impossible: I was sitting directly on top of the right main landing gear. The cabin itself felt vast, the overhead bins disappearing into the ceiling without intrusion. This machine wasn't just engineered; it was designed, with a palpable sense of the human who would inhabit it.",
        "Then came the pushback, and the world outside went quiet. As the pilots ran their checklist, the wing came alive. Slats and flaps extended to the `1+F` takeoff configuration, a complex choreography of surfaces creating the perfect shape for lift. The two massive Rolls-Royce Trent XWB engines began to breathe, and my mind went away. I wasn't a passenger anymore. I was inside the machine's mind, imagining myself writing the code for the start sequence.",
        "*Initial state: APU bleed air ON. Command: Open starter valve.* I felt the faint vibration as the N2 spool began to turn, its sound a deep, almost silent hum, nothing like the metallic scream of older jets. *Condition: N2 rotation > 25%. Command: Introduce fuel, fire igniters.* There was no sudden kick, no audible pop as the fuel ignited—just a seamless, swelling surge of power as the engine spun up and sustained itself. It was the perfect execution of a software sequence, the pilot's intent translated into reality by a network of microcontrollers hidden beneath the floor.",
        "The pushback master gave his signature wave, and we taxied. From my perch atop the landing gear, I could feel everything. Every touch of the brakes by the pilot resonated through the floor, the complex six-wheel bogie articulating through the turns, managed by a brake-by-wire system that felt both precise and alive.",
        "Lined up on Runway 18, cleared for an immediate takeoff. The captain unleashed the engines. The windsock was ramrod straight, a gift of a headwind. As we surged forward, I saw it. The wing *flexed*. Not a shudder, but a deep, dramatic, beautiful arc. The engine nacelle on its pylon trembled, absorbing the immense forces—a sight I've never witnessed on another aircraft. Before my pilot's brain could even whisper \"V1,\" we were rotating, hurled into the sky by the wind.",
        "And then the feeling hit me, a profound, almost shocking realization. For the first time in my life, I was being carried aloft not by metal, but by wings of woven carbon fiber. It was a new kind of strength, a new sensation of flight. Eight minutes later, the wing was clean, the climb was effortless, and we banked right, setting course for Addis.",
        "Even in turbulence, the A350 was a revelation. The pilot made a few sharp turns to avoid the worst of the dirty air, but when we hit the bumps, it wasn't a jarring ordeal. It was a beautiful dance. From my seat, I watched the wingtips flex gracefully, absorbing the energy, while the fuselage swayed in a gentle, coordinated rhythm. I was a partner in this dance, feeling the machine respond to the sky not with brute force, but with an intelligent, responsive grace.",
        "The descent into Addis Ababa for runway 25L was the final act. From my position, I could hear the lifeblood of the aircraft at work. A series of deep, hydraulic thumps and whirs resonated from below as the landing gear pressurized and locked into place. On touchdown, the captain was keen not to brake harshly. There was no sudden, aggressive deceleration, just a long, smooth rollout, the auto-brakes and reverse thrust working in perfect harmony. It was the final, quiet testament to the machine's sophistication.",
        "### A Brief Layover, A Shift in Perspective",
        "The layover in Addis Ababa was a frantic 30 minutes—just enough time to deplane and race to the next gate. In that short walk, I was transitioning between more than just two airplanes; I was transitioning between two eras of aviation design. The air still hummed with the quiet power of the A350, but my destination was a different machine entirely.",
        "### The Legend and the Legacy: Boarding the 737 MAX",
        "Stepping onto the 737 MAX, aircraft ET-AVX, was an immediate, visceral shift. My seat was 27L, but someone was already in it. After a brief shuffle, I settled in, my frame struggling to fit in a way it never had on the A350. The narrow-body cabin is familiar, a classic design honed over decades, but it's impossible to board this particular aircraft without a profound sense of gravity.",
        "We taxied back out to the same runway, 25L. As we held short, a Boeing 777-ER, the MAX's bigger, older brother, thundered past us and climbed into the sky to do what she was meant to do: dance. Then, it was our turn.",
        "The flight to Kigali was completely full. As we lined up, all I could think about was that from this exact spot, on a Sunday morning in March 2019, some people did not make it. The MAX failed them. The world was quick to judge the Ethiopian pilots, to whisper about inexperience, only for the truth to emerge later—a story of software, sensors, and a system that betrayed its crew. And here I was, on the same runway, on the same type of aircraft, now recertified and redeemed.",
        "The captain pushed the throttles forward. The takeoff roll felt long, powerful, eating up 75% of the runway with our heavy load. With every passing meter of concrete, my mind was on that other flight. It was a heavy feeling, a mix of an engineer's confidence in the fixes and a pilot's empathy for the crew who faced an impossible situation. This takeoff wasn't just a departure; it was an act of faith, a testament to the entire aviation industry's painful, public, and necessary process of correction. We climbed out into the sky, and the machine flew flawlessly. It was a somber, silent tribute.",
        "### Conclusion: A Question at 30,000 Feet",
        "The rest of the flight on the MAX was uneventful, but the landing in Kigali was a masterclass. I have been on most of Ethiopian's 737 flights, and their pilots have truly mastered this machine. It is not a landing; it is a *transition*. They seamlessly and effortlessly transition the aircraft from air to ground. A crosswind gave us a slight jarr to the right, which the pilot overcorrected with left rudder—a masterful display of skill.",
        "As I deplaned, the familiar question hit me, but this time it felt different, heavier. Should I transition from my Cessna 172s to these big jets? The struggle isn't just about choosing a career; it's about choosing an identity. From the 172, the obvious transition would be to the Cessna 208 Caravan, a masterpiece built for Africa with a soft spot in my heart. That is the more achievable goal. But if I push myself hard enough, the path leads to a much larger, more daunting question: would I leave my current career? Would I walk away from the joy of building things from the ground up—from packing a Linux box with network cards to make a BGP router, to designing the logic for an embedded system? I need to understand the fundamentals, the very soul of the machine.",
        "This journey gave me the answer. The A350 was a symphony of systems I longed to orchestrate. The 737 MAX was a stark reminder of the human who must ultimately be the master of the machine, no matter how complex the code. The two philosophies that flew me across Africa were the two philosophies battling inside my own head.",
        "And as my mind wanders, it always comes to the same conclusion. The goal isn't just to be in the left seat. It's to be the one who can explain the soul of the machine to the person who sits there. To truly satisfy all these passions—to understand the machine, to fly it, and to teach others—the path becomes clear. To become an instructor for an airline or a manufacturer is to become the bridge between the silicon and the sky. It’s the ultimate form of systems engineering. Perhaps that is the transition that truly matters."
    ]
    
    return {
        "id": "two-flights-two-philosophies",
        "title": title,
        "category": "Aviation",
        "content": content
    }

def main():
    """
    Main execution function to add the new article.
    """
    updater = ArticleUpdater()
    
    # Get the new article data
    new_article = get_flight_article_data()
    
    # Add the article
    updater.add_article(new_article)
    
    # List all articles to confirm
    updater.list_articles()

if __name__ == "__main__":
    main()
