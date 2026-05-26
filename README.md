# TTWargame_Analyzer

A tool for visualizing and analyzing distributions of outcomes for tabletop wargames.

## Data Structures

### Results

#### Pre-Plotting

```javascript
data: {
    [rollResult(NUMBER)]: probability(NUMBER)
}
```

## Endpoints

- /
- /home
- /tests/plot

## Running the app

Initializing the Database:
`flask --app flaskr init-db`

Standard:
`flask --app flaskr run`

Debug Mode:
`flask --app flaskr run --debug`

Hosted on <http://127.0.0.1:5000/>

## TODOs

## Ideas

- Use strategy patterns to represent abilities, weapon keywords, etc.
- Use factory patterns to instantiate weapons, models, units, etc from user inputs.

- Think of the system as an assembly line, creating distributions to match user specifications

- Use PyQt6 for GUI (due to licensing)

## Dependencies

    └ Flask (pip install Flask) <br>
        └ dotenv (pip install python-dotenv)
