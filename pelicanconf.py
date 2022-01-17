AUTHOR = 'Shailesh Kumar'
SITENAME = 'In Digits'
SITEURL = ''

PATH = 'content'

THEME = "elegant"

TIMEZONE = 'Asia/Kolkata'
DATE_FORMATS = {"en": "%b %d, %Y"}

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
         ('Optimization Book', 'https://convex.indigits.com'),
         ('CR-Sparse', 'https://github.com/carnotresearch/cr-sparse'),
         ('Interra', 'https://interrasystems.com'),
         ('JAX', 'https://github.com/google/jax'),
         )

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/shailesh1729'),
          ('github', 'http://github.com/shailesh1729'),
          ('linkedin', 'https://www.linkedin.com/in/shaileshkumar1729'),
          ('facebook', 'https://www.facebook.com/shailesh.kumar.9484'),
          ('youtube', 'https://www.youtube.com/channel/UC_cwiJQwHSDlDl-IGnu-0fw'),
          ('medium', 'https://shaileshk.medium.com'),
          )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Defaults
DEFAULT_CATEGORY = "Miscellaneous"
USE_FOLDER_AS_CATEGORY = False
ARTICLE_URL = "{slug}"
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"
TAGS_URL = "tags"
CATEGORIES_URL = "categories"
ARCHIVES_URL = "archives"
SEARCH_URL = "search"

SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}


DIRECT_TEMPLATES = ["index", "tags", "categories", "archives", "search", "404"]
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
USE_SHORTCUT_ICONS = True


# Elegant Labels
SOCIAL_PROFILE_LABEL = "Stay in Touch"
RELATED_POSTS_LABEL = "Keep Reading"
SHARE_POST_INTRO = "Like this post? Share on:"
COMMENTS_INTRO = "So what do you think? Did I miss something? Is any part unclear? Leave your comments below."


# Email Subscriptions
EMAIL_SUBSCRIPTION_LABEL = "Get New Release Alert"
EMAIL_FIELD_PLACEHOLDER = "Enter your email..."
SUBSCRIBE_BUTTON_TITLE = "Notify me"

DISQUS_FILTER = True
UTTERANCES_FILTER = True
COMMENTBOX_FILTER = True


LANDING_PAGE_TITLE = "Musings of Shailesh Kumar"

PROJECTS_TITLE = "My Projects"
PROJECTS = [
    {
        "name": "CR-Sparse",
        "url": "https://github.com/carnotresearch/cr-sparse",
        "description": "Functional models and algorithms for sparse signal processing",
    },
    {
        "name": "Convex Optimization Book",
        "url": "https://github.com/shailesh1729/cvx-opt-book",
        "description": "A book on mathematics related to convex optimization for signal processing",
    },
]