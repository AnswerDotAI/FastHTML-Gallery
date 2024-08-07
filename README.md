# FastHTML-Gallery

This is a gallery of FastHTML components that shows common patterns in FastHTML apps. It includes minimal examples of chat bubbles, cascading dropdowns, interactive charts, and more.

## Running

To run the project, use the following command:

```bash
uvicorn main:app
```

## Contributing

### Adding an Example

The best way to contribute is by adding examples to the gallery.  There 2 options:

1. **Easy way:**  Open an issue with a link to the app code (gist, file in a github repo, etc.), and I will add it.  I am completely fine with this, so if the full contribution way would take more time than you have do this!
1. **Full Contribution Way:**  Open a PR with all the details needed for the site.  I can help through every step of this! 
  + Copy a similar example directory and do a PR with all the details needed for the site
  + **app.py**: Have a normal app, with 2 exceptions:
      + You must have a `homepage` function that generates the main page.  You can use `app.get('/'); def homepage():` 
      + Because the app will be submounted, `/` routes will be `/{dir_path}/` in your HTMX get/post/etc attributes.  You can see an example of this in the `cascading_dropdowns` example application.
   + **text.md**: This is an optional markdown file.  Good for adding links to references, docs, attribution, etc.
   + **metadata.ini**: Fill these out
   + **img.png**:  An image of your app for the main page card
   + **gif.gif**:  A gif of your app for the main page card (can be a copy of `img.png` if no dynamic content)
  + Run `uvicorn main:app` in the root of this git repo and check:
    + The main page card looks good (both in animations mode and not)
    + Your app works.  If not, it's possible the submounting routes thing above!

### Other Contributions

See issues for different things that need to be done to improve the project.

If you have any suggestions for improving this project, please open an issue, submit a pull request, or contact me on the FastHTML discord server.

Things on the list to do someday (PRs or discussions are welcome!).

+ Make the site prettier without making it too complicated
+ Hover over image to see gif
+ Add a way to organize gallery by content (headers, search, tags, idk).  PR welcome once 10+ examples exist.
+ Safe way to have users modify in the browser?  I'm unsure I want to do this, so you'd have to convince me.
+ Your idea?
