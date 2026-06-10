# All India Village Explorer

## Overview

A Flask + PostgreSQL based geographical data platform providing hierarchical access to Indian village data.

The platform allows users to navigate:

State → District → Subdistrict → Village

and perform village-level searches through REST APIs.

---

## Features

* State, District and Subdistrict hierarchy
* Village search functionality
* Village details API
* PostgreSQL relational database
* API key management
* API usage logging
* Dashboard analytics
* Dynamic frontend using HTML, CSS and JavaScript

---

## Tech Stack

* Flask
* PostgreSQL
* HTML
* CSS
* JavaScript
* REST APIs

---

## Database Statistics

* States: 2
* Districts: 17
* Subdistricts: 127
* Villages: 21,148+

---

## API Endpoints

* /states
* /districts/<state_id>
* /subdistricts/<district_id>
* /villages-by-subdistrict/<subdistrict_id>
* /search?q=village_name
* /village/<village_id>
* /dashboard

---

## Future Scope

* Complete India dataset
* Authentication and subscription plans
* Rate limiting
* Deployment on cloud
* API monetization
