# TTWargame_Analyzer
A tool for visualizing and analyzing distributions of outcomes for tabletop wargames.


## Ideas
- Use strategy patterns to represent abilities, weapon keywords, etc.
- Use factory patterns to instantiate weapons, models, units, etc from user inputs.

- Think of the system as an assembly line, creating distributions to match user specifications

- Use PyQt6 for GUI (due to licensing)

## TODOs
- Add scrollbar to lists when too many items are added
- Consolidate styles for unit list buttons (change style & cursor when hovered)
- Navigate to units/update when initially saving a unit (in units/create)
- Ensure units.update returns a valid http response in all cases
- Avoid re-rendering template when updating or creating unit fails (don't erase current inputs)

- restrict 'create' pages to key data (e.g. name), then upon creation redirect to corresponding 'update' page

## Endpoints
- /
- /create
- /<int:id>
- /delete/<int:id>

## Running the app
Initializing the Database:
    ``` flask --app flaskr init-db ```

Standard:
    ``` flask --app flaskr run ```

Debug Mode:
    ``` flask --app flaskr run --debug ```

Hosted on <http://127.0.0.1:5000/>


## Dependencies
    └ Flask (pip install Flask) <br>
        └ dotenv (pip install python-dotenv)
