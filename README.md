# FastHTML-Gallery

A gallery of FastHTML components to show common patterns in FastHTML apps.  It includes minimal examples of things like chat bubbles, cascading dropdowns, and more.

## Running

To run the project, use the following command:

```bash
uvicorn main:app
```

## Contributing

The best way to contribute is by adding examples to the gallery.  

To do this create a new directory in the `examples` directory.  It should include the following files:
+ **img.png:** A screenshot of the app for the card gallery
+ **app.py:** A FastHTML app that can be run with `uvicorn app:app`
+ **metadata.ini:** A config file with the following keys:
  + **REQUIRED:**
    + **ImageAltText:** Alt Text for your image that is displayed on the main gallery page
    + **ComponentName:** A short but descriptive name of the component that is displayed on the main gallery page
    + **ComponentDescription:** A short description of the component that is displayed on the main gallery page

If you have any suggestions for improving this project, please open an issue, submit a pull request, or contact me in the FastHTML discord server.

