# FastHTML-Gallery

This is a gallery of FastHTML components that shows common patterns in FastHTML apps. It includes minimal examples of chat bubbles, cascading dropdowns, interactive charts, and more.

## Setup

To install the dependencies:

```bash
pip install -r requirements.txt
```

## Running

To run the project, use the following command:

```bash
python main.py
```

## Contributing

### Adding an Example

One way to contribute is by adding examples to the gallery!

1. Create an app that servers as an example.  Make sure you can say in 1 simple sentence what the example is illustrating.
2. Create a new folder in an appropriate directory (e.g. `examples/widgets/` or `examples/visualizations/`) for your example.
3. Create an `app.py` file.  Things to know:
    + You should use route names or relative paths, not absolute paths.  This is because the app will be submounted, so the routes will be prefixed with the directory path.
    + The root route will be what is shown in the gallery
4. Add neccesary metadata
    + `card_thumbnail.png` and `card_thumbnail.gif` are used for the main page card.  Both are required.
    + `metadata.ini` is used to show the examples on the main page, look at a couple existing ones for examples of what information to include.
    + `info.md` is optional for examples, but required for apps.  This is where you can describe and provide information for how it works.  If this file exists an info page for the example will be created autoamticallyy
5. Run the full project with `python main.py`.  Check that your example card and all pages look good and load correctly.  Click into a couple others and make sure other pages load correctly too.


### Other Contributions

See issues for different things that need to be done to improve the project.

If you have any suggestions for improving this project, please open an issue, submit a pull request, or contact me on the FastHTML discord server.
