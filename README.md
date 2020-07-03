# instagramscrapper
Scrape data from the top profiles under a certain hashtag

# Project Description

A tool to find most prominent profiles under a certain hashtag or location on instagram and analyze their reach.

# Problem Statement

When reaching out to a target audience for effective marketing on instagram, it’s often quite hard to engage your audience.

Targeting and finding influencers of a certain community is a very tedious task that can get unmanageable very quickly. Although at the surface the task is very simple.

# Solution/Implementation

All the aforementioned actions can be easily performed by defining exact steps taken to identify an influencer. From the list of posts under a hashtag the most obvious candidates would be the ones with highest number of likes.

Since instagram doesn't allow conventional methods of scraping, It can be done by performing automated browser actions, by testing tools such as Selenium.

By defining the minimum number of likes per post I was able to guide my bot to scan through the posts and creating a CSV of all the profiles that met the criteria.

Then, this data is fed to the analysis tool, which reads instagram profiles in the CSV and scrapes the following metrics:

Average likes per post
- Number of posts
- Followers List
- Following List

I built the web scraping and automation tool using python. For automating actions like hover, click, page scroll etc. I used Selenium.

Read More [here](https://www.linkedin.com/pulse/scraping-instagram-selenuim-aman-khalid/)
