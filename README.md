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
+ **app.py:** A FastHTML app
    + Note:  This will be submounted, meaning `/blah` route will be `/{dir_name}/blah`.  When using htmx requests (ie `hx-get` attribute) you will need to use the full path to the route after submounting.
+ **metadata.ini:** A config file with the following keys:
  + **REQUIRED:**
    + **ImageAltText:** Alt Text for your image that is displayed on the main gallery page
    + **ComponentName:** A short but descriptive name of the component that is displayed on the main gallery page
    + **ComponentDescription:** A short description of the component that is displayed on the main gallery page

Once done, add you app as a submount in `main.py`.  Add your new mount to the routes list.

```python
app, rt = fast_app(hdrs=links, 
                   routes=[
                       Mount('/chat_bubble', create_display_page('examples/chat_bubble/', 'examples.chat_bubble.app')),
                       Mount('/cascading_dropdowns', create_display_page('examples/cascading_dropdowns/', 'examples.cascading_dropdowns.app')),
                   ])
```

If you have any suggestions for improving this project, please open an issue, submit a pull request, or contact me in the FastHTML discord server

Current top priority for improvement:

+ Add more examples

Things that are on the list, but I'm not actively working on (PRs or Isues discussing them welcome!)

+ Make site prettier without making it too complicated
+ Add a search bar and/or tagging to the gallery (PR welcome once 10+ examples exist)
+ Safe way to have users modify in browser?
+ Your idea?
