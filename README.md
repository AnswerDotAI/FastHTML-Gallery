# FastHTML-Gallery

A gallery of FastHTML components to show common patterns in FastHTML apps.  It includes minimal examples of things like chat bubbles, cascading dropdowns, and more.

## Running

To run the project, use the following command:

```bash
uvicorn main:app
```

## Contributing

### Adding an Example

The best way to contribute is by adding examples to the gallery.  

1. Copy `examples/_hello_world` and modify the contents to create your new example.
  + You must have a `homepage` function that generated the FastHTML for your app like in the Hello World example.
2. Submount your app by adding it to the `main.py` routes list following the hello_world convention
  + `Mount('/_hello_world', create_display_page('examples/_hello_world/', 'examples._hello_world.app'))`
3. Verify it looks good by running `uvicorn main:app` in the root of this git repo

> You app will be submounted, meaning `/blah` route will be `/{dir_name}/blah`.  When using htmx attributes (ie `hx-get` attribute) you will need to use the full path to the route after submounting.  You can see an example of this in the `examples/cascading_dropdowns` example application.

### Other Contributions

If you have any suggestions for improving this project, please open an issue, submit a pull request, or contact me in the FastHTML discord server

Current top priority for improvement:

+ Add more examples

Things that are on the list, but I'm not actively working on (PRs or discussions are welcome!)

+ Make the site prettier without making it too complicated
+ Add a search bar and/or tagging to the gallery (PR welcome once 10+ examples exist)
+ Safe way to have users modify in browser?  Not sure I want to do this so you'd have to convince me.
+ Your idea?
