# TTWargame_Analyzer
A tool for visualizing and analyzing distributions of outcomes for tabletop wargames.


## IDEAS
- Use strategy patterns to represent abilities, weapon keywords, etc.
- Use factory patterns to instantiate weapons, models, units, etc from user inputs.

- Think of the system as an assembly line, creating distributions to match user specifications

- Use PyQt6 for GUI (due to licensing)

## Endpoints
- /
- /create
- /<int:id>/update
- /<ind:id>/delete

## Running the app
Standard:
    ``` flask --app flaskr run ```

Debug Mode:
    ``` flask --app flaskr run --debug ```

Hosted on <http://127.0.0.1:5000/>


## Dependencies
    └ Flask (pip install Flask) <br>
        └ dotenv (pip install python dotenv)
