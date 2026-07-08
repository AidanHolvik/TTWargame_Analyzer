# TTWargame_Analyzer

A tool for visualizing and analyzing distributions of outcomes for tabletop wargames.

## Data Structures

### Regular Expressions

#### Dice roll or flat int value

```python
"^\d+(?i:D\d+)?(\+\d+)?$|^(?i:D\d+)(\+\d+)?$"
```

## Endpoints

- /
- /home
- /tests/plot
- /tests/weaponStats

## Running the app

Initializing the Database:
`flask --app flaskr init-db`

Standard:
`flask --app flaskr run`

Debug Mode:
`flask --app flaskr run --debug`

Hosted on <http://127.0.0.1:5000/>

## TODOs

- handle model/unit abilities which affect weapon stats and offensive rolls
- record model/unit keywords in the DB
- handle weapon keywords affecting offensive rolls (blocked by model/unit keywords)

## Ideas

- Use strategy patterns to represent abilities, weapon keywords, etc.
- Use factory patterns to instantiate weapons, models, units, etc from user inputs.

- Think of the system as an assembly line, creating distributions to match user specifications

- Use PyQt6 for GUI (due to licensing)

## Dependencies

```mermaid
    flowchart TD
    classDef missing stroke-dasharray: 5
    blinker["blinker<br/>1.9.0"]
    click_0["click<br/>8.4.2"]
    colorama["colorama<br/>0.4.6"]
    flask["Flask<br/>3.1.3"]
    itsdangerous["itsdangerous<br/>2.2.0"]
    jinja2["Jinja2<br/>3.1.6"]
    markupsafe["MarkupSafe<br/>3.0.3"]
    numpy["numpy<br/>2.5.0"]
    pip["pip<br/>26.1.2"]
    scipy["scipy<br/>1.18.0"]
    werkzeug["Werkzeug<br/>3.1.8"]
    click_0 -- "any" --> colorama
    flask -- ">=1.9.0" --> blinker
    flask -- ">=2.1.1" --> markupsafe
    flask -- ">=2.2.0" --> itsdangerous
    flask -- ">=3.1.0" --> werkzeug
    flask -- ">=3.1.2" --> jinja2
    flask -- ">=8.1.3" --> click_0
    jinja2 -- ">=2.0" --> markupsafe
    scipy -- ">=2.0.0,<2.8" --> numpy
    werkzeug -- ">=2.1.1" --> markupsafe
```
