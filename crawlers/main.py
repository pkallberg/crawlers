# main.py

import scrapy.crawler
import scrapy.utils.project
import click

from . import spiders, utils
from .settings import CLIOptions
from .database import queries


SPIDERS = {
    "com": spiders.yelp.yelp_us.USProfileSpider,
    "pt": spiders.yelp.yelp_pt.PTProfileSpider
}


@click.command()
@click.option(
    CLIOptions.profile_url.value,
    default=None,
    type=str,
    help="Yelp profile for crawling"
)
@click.option(
    CLIOptions.list_url.value,
    default=None,
    type=str,
    help="List of yelp profiles for crawling"
)
def run_yelp_spider(profile_url: str = None, list_url: str = None) -> None:

    if not(profile_url or list_url):
        print(utils.cli_help())
        exit()

    # Init spider process
    from_list = True if list_url else False
    url = list_url if list_url else profile_url
    spider = SPIDERS.get(utils.yelp_tld(url=url))

    if spider:
        process = scrapy.crawler.CrawlerProcess(
            scrapy.utils.project.get_project_settings()
        )
        process.crawl(spider, url=url, list_url=from_list)
        process.start()
    else:
        raise Exception(
            f"Not Implemented: {utils.yelp_tld(url=url)} website"
        )


if __name__ == "__main__":
    if not queries.create_profiles_table():
        raise Exception("DBError: Unable to create profiles table")
    run_yelp_spider()
