# Fit Market Calculator Design

## Introduction
### Purpose of the system
Fit Market Calculator is a market data tool designed for Eve Online, an internet
spaceship game. The primary use of this tool is to expose data for three 
reasons:

1) Simulating the market effects of a large number of fits being purchased
at the same time. This often happens when blocs change doctrines or go to war.
Fitting teams may be interested in knowing, for a particular fit, exactly what
effects on the market will be if they try to buy hundreds or thousands of that
fit in a short time period.

2) Market arbitrage, such as the type normally legally performed at
trading firms. In the real world, this might look like an automated purchase of
a commodity in one market, an electronic transfer of assets to another
market, and a quick sale at a profit. In Eve, this is often regional
arbitrage- taking advantage of pricing discrepancies in different markets
where the profits are able to cover shipping costs.

3) Market manipulation, such as the type 
[illegally performed](https://en.wikipedia.org/wiki/Libor_scandal) at trading
firms. In game, market manipulation is within rules and practiced frequently.
Since short sales are not allowed, this means using ingenuity to:
 - corner markets on scarce items, 
 - slowly flood markets to discourage manufacturing of long-lead-time items
   until a market is monopolized before spiking prices,
 - capitalizing on situations where a large number of ships that may need 
 replacing use a rare module,
 - or other original inventive schemes.
 
### Design Goals
1) Gather data for machine learning exercises.
2) Keep hosting costs low by utilizing on-demand compute time.

### Definitions, acronyms, and abbreviations
Account - An Eve account. Each account is managed by Eve and has no bearing
on our application usage. Instead, we assign values to characters.
An Account may have up to 3 characters.

Alliance - An alliance object within Eve Online. A collection of corporations
organized within the game.

Character - A character object within Eve Online.
An Account may have up to 3 characters.

Corporation - A corporation object within Eve Online. A collection of characters
socially self-organized.

CCP - The company that makes Eve Online

Eve - An internet spaceship game

Fit - A collection of items; most often a ship and its component parts

FMC - Fit Market Calculator

Tenant - An individual or organization deploying an installation of FMC. This
must be a character, corporation, or alliance recognized in game by the Eve
API server.

### References
[ESI Swagger Docs](https://esi.evetech.net/ui)
[ESI Third Party Docs](https://eveonline-third-party-documentation.readthedocs.io/en/latest/esi/)

## Proposed Software Architecture

### Overview
In supporting our data gathering and cost-conscious goals, we will use DynamoDB
for persistent storage, Lambda for recurring data scraping and map reduce
workers, and Lambda again for processing REST requests. The web app will be 
served by a CDN such as CloudFlare.

### Subsystem Decomposition
**Item Scraper**: An infrequently recurring process that will update the full
list of market items. This will not be run more frequently than daily since the
list will likely be only very infrequently updated.

**Order Scraper**: A frequently recurring process that will, each 15 minutes, 
gather order data on all market products. After scraping all data, a digest of 
the data useful for market analysis will be generated.

**REST API**: An HTTP service used for serving digested data for market
analysis.

**Web App**: ReactJS application used for displaying digested market data
in a user friendly way.

### Persistent Data Management
DynamoDB will be used. It is a persistent cloud RDBMS with a 25GB free tier, 
likely sufficient for the foreseeable future.

### Access Control
Specific permissions will be ignored by this application. A character will
either have access or not.

To avoid complicated authentication schemes and focus on feature delivery,
access control will be as simple as possible. In keeping with the theme of
relying on Eve's API servers for data, we will also use its OAuth2
service for identifying characters. If a user logs in with a character via
the Eve OAuth server, the character name will be checked against of source-
controlled config file for a matching character name, corporation name,
or alliance name. All access allowances will be by one of these 3 whitelists.

### Security
OWasp Top 10 issues will be avoided.

A1, Injection, will be avoided by using SQLAlchemy. SQL operations
will all be parameterized.

A2, Broken Authentication, will be mostly* avoided by relying on the might
of CCP for character name authentication. Brute force, weak passwords, 
credential recovery, password hashing, and MFA are all handled on their servers
as a service. Session IDs will not be used.

A3, Sensitive Data Expose, will be mitigated by SSL. Due to the relatively
worthless nature of video game data and the lack of authentication-related
data being stored by our application, the only piece of sensitive data is the
OAuth token stored by the user. Even if this is compromised, data exposure
risks are limited.

A4, XXE, is mitigated by nature of not parsing XML.

A5, Broken Access Control, will be mitigated by a specific suite of integration
tests to check for account isolation.

A6, Security Misconfiguration, is outside the direct control of the application.
Documentation will be provided to allow entities to properly configure the
application and configuration options will be extremely limited and clearly
expressed.

A7, XSS, will be mitigated by not loading data from untrusted sources.

A8, Insecure Deserialization, will be mitigated by using Flask for string
handling and SQL queries will be parameterized by SQLAlchemy.

A9, Using Components with Known Vulnerabilities, requires cooperation of both
internal development staff and entities running the software. Code reviews will
include a quick audit of changed dependencies with updates or removals where
necessary. Occasional dependency audits may identify abandoned dependencies that
should be refactored out of the code base.

A10, Insufficient Logging & Monitoring, will be mitigated by using AWS 
CloudWatch. All logs will use a common format and common timezone for easy
tracing. Alerts will be handled by CloudWatch policies.

