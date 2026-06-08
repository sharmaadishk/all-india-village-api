# All India Village API

A REST API built using Flask and PostgreSQL to provide hierarchical Indian geographical data.

## Features

* State API
* District API
* Subdistrict API
* Village API
* Search API
* PostgreSQL Integration
* Hierarchical Data Structure

## Tech Stack

* Python
* Flask
* PostgreSQL
* Pandas
* psycopg2

## Dataset

Government MDDS Village Dataset

## Implemented APIs

### Health Check

GET /health

### States

GET /states

### Districts

GET /districts

### Subdistricts

GET /subdistricts

### Villages

GET /villages

### Search Villages

GET /search?q=ari

## Database Structure

Country
→ State
→ District
→ Subdistrict
→ Village

## Current Progress

* Sikkim dataset imported
* 452 villages imported
* Search functionality implemented
* REST APIs operational

## Future Improvements

* Full India dataset import
* Authentication & API Keys
* Rate Limiting
* Redis Caching
* React Dashboard
* Analytics Panel
