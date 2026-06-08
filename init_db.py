import sqlite3

# We name the database to match the brand
DB_FILE = 'ecommdots.db'

def build_architecture():
    # Establish connection to the database file (creates it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Building database architecture...")

    # 1. Forge the Articles Table matching your exact custom UI requirements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            read_time INTEGER NOT NULL,
            publish_date TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT, 
            author_name TEXT NOT NULL,
            author_image TEXT NOT NULL,
            thumbnail_url TEXT NOT NULL,
            is_wide BOOLEAN NOT NULL DEFAULT 0,
            is_featured BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Forge the Secure Users Table for the CMS Dashboard
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # 3. Clear existing seed data (if script is run multiple times)
    cursor.execute('DELETE FROM articles')

    print("Extracting and seeding Ecommdots Intelligence Vault data...")

    # The exact data extracted from your static HTML
    seed_data = [
        # THE FEATURED ARTICLE
        (
            "THE Q4 ALGORITHMIC PLAYBOOK FOR 8-FIGURE BRANDS", "q4-algorithmic-playbook", 
            "Amazon Strategy", "Amazon Strategy", 14, "June 2025",
            "Stop guessing. This teardown exposes the exact FBA inventory flows, dynamic bidding cadences, and defensive keyword moats that the top 1% of Amazon sellers deploy when competition peaks — and how to copy every single one of them.",
            "<p>Full article content goes here...</p>", "Saif Ur Rehman", 
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",
            False, True
        ),
        # GRID ARTICLE 1 (WIDE)
        (
            "BEYOND BASIC RETARGETING: HOW 8-FIGURE BRANDS STEAL OFF-PLATFORM TRAFFIC", "beyond-basic-retargeting",
            "PPC & Ads", "Advanced", 11, "May 2025",
            "How elite brands leverage Amazon DSP to intercept competitor browsers off-platform and funnel them into hyper-optimized storefronts before the competitor even knows they're gone.",
            "<p>Full article content goes here...</p>", "Muhammad Arslan",
            "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
            True, False
        ),
        # GRID ARTICLE 2
        (
            "AESTHETICS THAT CONVERT: THE PSYCHOLOGY BEHIND OUR BEST VISUALS", "aesthetics-that-convert",
            "Creative Studio", "Creative", 8, "May 2025",
            "Beautiful images don't sell products — strategically engineered visual funnels do. A deep dive into consumer psychology and exactly how we design main images that steal clicks.",
            "<p>Full article content goes here...</p>", "Muhammad Farhan",
            "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&w=600&q=80",
            False, False
        ),
        # GRID ARTICLE 3
        (
            "THE 40% COGS REDUCTION FRAMEWORK WE USE FOR EVERY CLIENT", "40-percent-cogs-reduction",
            "Sourcing", "Operations", 10, "April 2025",
            "Margin is won or lost in the supply chain. Here's the exact negotiation framework we use to slash manufacturing costs without compromising on product quality.",
            "<p>Full article content goes here...</p>", "Saif Ur Rehman",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=600&q=80",
            False, False
        ),
        # GRID ARTICLE 4
        (
            "BRAND REGISTRY DECODED: YOUR COMPLETE FORTRESS BLUEPRINT", "brand-registry-decoded",
            "Brand Building", "Protection", 9, "April 2025",
            "From trademark filing to IP Accelerator fast-tracking — the complete operational guide to locking down your brand and eliminating Buy Box hijackers permanently.",
            "<p>Full article content goes here...</p>", "Abdul Moeed",
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1614064641913-a53f910ea1eb?auto=format&fit=crop&w=600&q=80",
            False, False
        ),
        # GRID ARTICLE 5 (CASE STUDY)
        (
            "EARTH FED MUSCLE: 6.2× ROAS IN 90 DAYS", "earth-fed-muscle-case-study",
            "Case Study", "Case Study", 12, "March 2025",
            "A full breakdown of how we transformed a scattered ad architecture into a profit machine, scaling Subscribe & Save by 85% and hitting $2.4M in Q4 revenue.",
            "<p>Full article content goes here...</p>", "Saif Ur Rehman",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=600&q=80",
            False, False
        ),
        # GRID ARTICLE 6
        (
            "ACOS VS TACOS: THE METRIC THAT ACTUALLY MATTERS FOR NET PROFIT", "acos-vs-tacos-metric",
            "PPC & Ads", "Performance", 7, "March 2025",
            "Amazon's default reporting is engineered to make you spend more. Here's how to cut through the noise and measure what actually impacts your bottom line profitability.",
            "<p>Full article content goes here...</p>", "Muhammad Arslan",
            "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=600&q=80",
            False, False
        ),
        # GRID ARTICLE 7 (WIDE)
        (
            "STRATEGY DETHRONES THE ALGORITHM: WHY CHASING A9 IS A LOSING GAME", "strategy-dethrones-algorithm",
            "Amazon Strategy", "Deep Dive", 15, "February 2025",
            "Everyone chases the A9 algorithm. We build brand moats. A deep-dive manifesto on why the brands that win long-term focus on category authority rather than algorithmic shortcuts — and the five tactical frameworks to build one.",
            "<p>Full article content goes here...</p>", "Saif Ur Rehman",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1612296727716-d6c69d2a2cbb?auto=format&fit=crop&w=1200&q=80",
            True, False
        ),
        # GRID ARTICLE 8
        (
            "A+ CONTENT MODULES THAT ELIMINATE BUYER OBJECTIONS IN 3 SECONDS", "aplus-content-modules",
            "Creative Studio", "Design", 6, "January 2025",
            "The psychological stacking sequence behind our highest-converting A+ layouts — and the exact module order that removes hesitation at each stage of the buy decision.",
            "<p>Full article content goes here...</p>", "Abdul Wahab",
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=600&q=80",
            False, False
        ),
        # GRID ARTICLE 9
        (
            "THE ZERO-TO-RANK LAUNCH SYSTEM: PAGE 1 IN 30 DAYS", "zero-to-rank-launch-system",
            "Amazon Strategy", "Launch", 13, "January 2025",
            "The precise launch cadence — from honeymoon period exploitation to review velocity engineering — that we deploy on every new product to hit page 1 within a single month.",
            "<p>Full article content goes here...</p>", "Saif Ur Rehman",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80",
            "https://images.unsplash.com/photo-1609921212029-bb5a28e60960?auto=format&fit=crop&w=600&q=80",
            False, False
        )
    ]

    cursor.executemany('''
        INSERT INTO articles (
            title, slug, category, subcategory, read_time, publish_date, 
            excerpt, content, author_name, author_image, thumbnail_url, is_wide, is_featured
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', seed_data)

    conn.commit()
    conn.close()
    print(f"Success! {len(seed_data)} articles professionally embedded into the database.")

if __name__ == '__main__':
    build_architecture()