#!/usr/bin/env python3
"""
Article Updater for Daudi's Blog
This script adds the new "Building Africa's Nervous System" article to the blog data.
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

def get_afpif_article_data() -> Dict[str, Any]:
    """
    Contains the data for the 'Building Africa's Nervous System' article.
    """
    title = "Building Africa's Nervous System: Reflections from AfPIF 2025"
    # Content is split into paragraphs (strings in a list)
    content = [
        "Standing in Nigeria, I felt the echo of history beneath my feet. This land was not just a modern nation; it was a nexus in the vast West African trade network, an empire of commerce that predated modern history. Centuries ago, caravans—the terrestrial fiber of their day—crisscrossed this region, carrying not just gold and salt, but culture, knowledge, and influence. Cities like Timbuktu and Gao were the great data centers, the IXPs where value was exchanged and amplified. When Mansa Musa made his pilgrimage, the world wasn't just stunned by his wealth; they were awakened to the existence of a sophisticated, self-sufficient economic system. He put his network on the global map.",
        "For me, hosting the African Peering and Interconnection Forum (AfPIF) 2025 here felt like a deliberate act of historical reconnection. The new gold and salt are data and connectivity. The new caravans are fiber optic cables. And the discussions in the room, whether the participants articulated it this way or not, were about a single, profound goal: to rebuild those ancient, powerful trade routes for the digital age and put Africa back on the map, not as a consumer of external networks, but as the master of its own. My last article, \"The Internet in Africa is Just a Connection to Europe,\" was a thesis from 30,000 feet. This week, on the ground, I saw the collision of that theory with our historical reality.",
        "The Vibe in the Room",
        "I listened as the hyperscalers—AWS, Meta, Google—delivered a consistent and clear message: \"We are interested in Africa, but there is work you need to do. Organize your networks. Grow the local fabric, the inland terrestrial fiber, and we will come.\" It was a conversation heavy with opportunity, but also with a familiar sense of frustration.",
        "Being physically in the room was validating. A presentation from Telegeography put a hard number on the feeling we all have: for the last five years, around 80% of Africa's total international connectivity has been with Europe. The philosophy I continue to talk about isn't just a philosophy; it's a statistical reality. For all the progress we've made, cloud access continues to be the primary driver for that external traffic. We are not building networks for ourselves; we are building them to attract the hyperscalers.",
        "Ethiopia, with its rapidly growing population approaching 130 million people, according to the United Nations Population Fund, was a topic of great interest—a massive, newly opened digital marketplace. Yet, who is laying the groundwork to actually reach those people? The conversation then hit closer to home. I am from Uganda, a landlocked nation. My country, along with our neighbors in Western DRC, Southern Sudan, Burundi, and Rwanda, connects to the world primarily through terrestrial fiber routes to Nairobi and, subsequently, the submarine cable landing stations in Mombasa—a dependency confirmed by network operators like Liquid Intelligent Technologies in their own infrastructure announcements. I am being told my local IXP and all our aggregated traffic is insignificant to attract the CDNs we so desperately need. Yet, Kenya's digital economy continues to grow because our collective demand is what drives their numbers up. How do we shout this from the mountains? How do we get the large CDNs to take a risk on Uganda?",
        "Over coffee, I sat with representatives from MTN, RENU, and the UIXP. The ideas were flowing. \"We need another IX in Uganda,\" one said, \"but it must not be in a telco's building. It must be carrier-neutral.\" The insight was brilliant, the need was urgent. But I had to ask: \"Why did we travel 6,500 kilometers, leave our country, to have this conversation here? Shouldn't we be having it at home?\"",
        "A Digital Identity",
        "The big push at the forum was for more Autonomous System Numbers (ASNs) and personal IP space. AFRINIC's own statistics show that Africa has roughly 2,500 allocated ASNs, a tiny fraction of the 100,000+ that form the global internet. As a passionate knowledge-sharer and educator on this continent, I feel this number reflects my own failures. Have I done enough to grow more engineers? Have I done enough to evangelize how the internet works and how we can grow these numbers to a point where they serve us?",
        "Are the younger generations being taught how to build the African internet—how to build Africa's nervous system? Or am I being naive? Is there something deeper I am not seeing? The bigger picture is that when an individual or a small business gets their own ASN and IP space, they stop being a mere statistic behind a large ISP. They become a nerve ending. They become a tangible part of the nervous system we are trying to lay the foundation for.",
        "The Nervous System and the Lymph Nodes",
        "I believe the IXPs should be supported to do what they do best: exchange local traffic and be the driving force for all the local ASNs on the ground. It makes me ask, how many ASNs are in the capital of my home area, Soroti? How many local businesses are \"trading\" online using their own ASN and IP space?",
        "We each need to be deliberate about creating as many nerve endings as possible so that Africa can get back to feeling and learning about her own body, network by network, IXP by IXP. Africa has a soul. For us to awaken that soul, we must wake her up from the extremities. Rather than continue to allow the \"brain\" to exist in Europe, let's build the brain here. As an embedded engineer, I am frustrated at the slow growth of this organism. I may be naive, but in as much as these things take time, I believe history will judge us very harshly for what we saw and did not correct. This is analogous to the ship that headed to the iceberg despite numerous calls to change course. We may not have invented much as this generation and are merely consumers, but let's take that data we are consuming and do something with it. For me, I see us being able to build this organism, but I am frustrated by what we are doing with what we have.",
        "A Pause to Action",
        "AfPIF left me with a profound sense of duty, a pause not of inaction, but of deliberate preparation. It crystallized the challenge I have set for myself. The power to build this nervous system doesn't lie solely with the hyperscalers, who serve their own purpose. It lies with the open-source community, with the educators, with the engineers on the ground who believe in real change.",
        "This forum was my opening statement for what must be done. It was also a place for me to solicit help. My commitment is this: I will document my progress in this mission, starting with the simplest of acts—asking the network engineers around me, one by one, \"Do you know what an AS number is? Do you know how the internet truly works?\"",
        "My goal is to help grow Africa to a point where we trade not just with company names, but with AS numbers. An ASN is more than a number; it is a declaration of digital sovereignty. It is your identity, your plot of land in the digital world. By claiming this space, we ensure each part of our rich cultural tapestry and diversity is represented online. The work is immense, but the ancient caravans were not built in a day. They were built one step, one route, one connection at a time. It is time to begin our journey.",
        "Sources",
        "* Africa-Europe Traffic: TeleGeography, \"African Network Geography Update,\" AfPIF 2023 Presentation.",
        "* Ethiopia Population: United Nations Population Fund, \"World Population Dashboard - Ethiopia,\" 2025 Data.",
        "* East Africa Connectivity: Liquid Intelligent Technologies, \"Announces the upgrade of its 1,300km fibre route,\" September 11, 2024. Press release detailing the Mombasa-to-Uganda-border route as critical for regional connectivity.",
        "* ASN Data: AFRINIC Statistics Portal (for African numbers) and aggregated global data from sources including the CIDR Report (for the 100,000+ global figure)."
    ]
    
    return {
        "id": "building-africas-nervous-system",
        "title": title,
        "category": "Networks",
        "content": content
    }

def main():
    """
    Main execution function to add the new article.
    """
    updater = ArticleUpdater()
    
    # Get the new article data
    new_article = get_afpif_article_data()
    
    # Add the article
    updater.add_article(new_article)
    
    # List all articles to confirm
    updater.list_articles()

if __name__ == "__main__":
    main()
