KNOWN_ARTIST_WORD_INSIGHT_ROMEO_SANTOS = """
        - Romeo Santos similarly emphasizes his name and the term "king," which may indicate a high opinion of himself.
        - Romeo Santos prefers to call women "Mami."
"""

KNOWN_ARTIST_WORD_INSIGHT_PRINCE_ROYCE = """
        - Prince Royce often emphasizes his name.
        - Prince Royce frequently refers to women as "Baby."
"""

KNOWN_ARTIST_WORD_INSIGHT_AVENTURA = """
        - Aventura also highlights their band name, which is fitting given that Romeo Santos is a member of the group.          
"""

KNOWN_ARTIST_THEME_INSIGHT_ROMEO_SANTOS = """
        - Romeo Santos' music deals a lot with contemplating the human 'inner world' and his lyrics often delve into complex emotions.
"""

KNOWN_ARTIST_THEME_INSIGHT_PRINCE_ROYCE = """
        - One of Prince Royce's musical themes is 'Forbidden Love' which usually involves falling in love with an unavailable person and focuses on the emotional highs and the thrill of love.
"""

KNOWN_ARTIST_THEME_INSIGHT_AVENTURA = """
        - One of Aventura's musical themes is 'Desire for Deeper Connection', which may reflects the songwriter's inclination toward having superficial relationships.
"""

def get_specific_artist_insights(artist_name):
    if artist_name.lower() == "romeo santos":
        return KNOWN_ARTIST_WORD_INSIGHT_ROMEO_SANTOS, KNOWN_ARTIST_THEME_INSIGHT_ROMEO_SANTOS

    elif artist_name.lower() == "prince royce":
        return KNOWN_ARTIST_WORD_INSIGHT_PRINCE_ROYCE , KNOWN_ARTIST_THEME_INSIGHT_PRINCE_ROYCE

    elif artist_name.lower() == "aventura":
        return KNOWN_ARTIST_WORD_INSIGHT_AVENTURA, KNOWN_ARTIST_THEME_INSIGHT_AVENTURA

    else:
        return "",""
