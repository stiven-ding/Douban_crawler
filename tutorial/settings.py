# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'
#SPLASH_URL = 'http://localhost:8050'
#DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
#HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# allow duplicates
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; http://www.google.com/bot.html) Chrome/W.X.Y.Z‡ Safari/537.36'

#USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    'scrapy_random_fake_ua.middleware.RandomUserAgentMiddleware': 400,
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #'tutorial.middlewares.TooManyRequestsRetryMiddleware': 543
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_MAX_CONTEXTS = 1
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 5
#CONCURRENT_REQUESTS = 10
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT=40 * 1000
COOKIES_ENABLED = True
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
    "timeout": 30 * 1000,  # 20 seconds
    "proxy": {
        'server': 'socks5://127.0.0.1:7890',
        'username': '',
        'password': ''
    }
}
PLAYWRIGHT_CONTEXTS = {
    "persistent": {
        "user_data_dir": "/Users/stivending/Library/Application Support/Chromium/Default/",
        #"java_script_enabled": True,
        "headless": False
    }
}

PLAYWRIGHT_ACCEPT_REQUEST_PREDICATE_TYPE = ["image", "Doc", "Media"]

#DOWNLOADER_MIDDLEWARES = {  
#    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#    'tutorial.middlewares.TooManyRequestsRetryMiddleware': 543,   
#    'scrapy_random_fake_ua.middleware.RandomUserAgentMiddleware': 400,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

RETRY_HTTP_CODES = [429, 403, 302]

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tutorial.pipelines.TutorialPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 0.2
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 1
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
