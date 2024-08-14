# Cellular Automata

Cellular automata are a class of models that are used to simulate complex systems. Cellular automata are used in a wide range of applications, including modeling the spread of diseases, traffic flow, and the behavior of crowds. This project is a 1 dimensional cellular automata. 

## How it works

We start with an initial row. In this app the row is a series of white squares followed by a single black square followed by more white squares. 

A cell is created based on the state of the three cells above it ( directly above and to the left and right). That means there are eight possible combinations of the three cells. We consider a white square to be a 0 and a black square to be a 1. This gives us a number between 0 and 7, I'll call this the cell update number.

The rule is a number between 0 and 255 (inclusive). We take that number and convert it to its binary representation. This will be a sequence of 8x 0s and 1s. Taking the cell update number, we look at the corresponding digit in the rule. If it is a 1, the cell becomes black, if it is a 0, the cell becomes white.

You can see a visual representation of the rule in the app. 

## User Interface

The app provides three main inputs:

- Rule Number (0-255): Determines the cellular automata rule
- Number of Generations (1-200): Sets how many rows will be generated
- Width (1-200): Defines the width of the grid

## Visualization

The cellular automata is visualized as a grid of white and black boxes, representing the 0 and 1 states respectively. The grid is dynamically updated using HTMX polling, creating an animated effect as new generations are added.

## Key Technologies and Techniques

* **HTMX Polling**: We use polling to update the grid every 100ms. This is done by setting the `hx-get` attribute `every .1s`. This triggers a GET request until we run out of generations and then the `Response(status_code=286)` stops the polling.  See the [HTMX documentation for polling](https://htmx.org/docs/#polling)

* **Progress Bar**:  A progress bar that shows the progress of the cellular automata.  Check out the [FastHTML Gallery page for progress bars!](https://fasthtml.gallery/widgets/progress_bar/display)

* **Show Hide Button**: A button that shows and hides the rule number.  Check out the [FastHTML Gallery page for show hide buttons!](https://fasthtml.gallery/widgets/show_hide/display)

* **Inline Input Validation**:  Real-time validation for rule number, generations, and width inputs.  Check out the [FastHTML Gallery page for inline validation!](https://fasthtml.gallery/dynamic_user_interface/inline_validation/display)

+ **Dynamic Grid Generation**: The automata grid is generated row by row, creating an animated effect.

### Server-Side Logic

The app uses FastHTML to define routes and handle the cellular automata logic on the server. Key routes include:

- `/`: The main page that renders the initial form and explanation.
- `/run`: Initializes and runs the cellular automata based on user input.
- `/next`: Generates the next row of the automata.
- `/validate/*`: Handles input validation for rule number, generations, and width.
- `/show_rule`: Toggles the display of the rule visualization.

### State Management

The automata state is managed server-side using a generator function:

- `generator`: A global variable dict that stores the cellular automata generator for each session.
- `run()`: A yields each automata generation.

### Dynamic Content

HTMX is used extensively to create a dynamic user interface:

- `hx-get` attributes trigger GET requests for various actions like running the automata or showing/hiding the rule.
- `hx-post` is used for inline validation of user inputs.
- `hx-target` specifies where the response from the server should be inserted.
- `hx-swap` determines how the new content should replace the old content. Various swap methods are used, including `outerHTML` and `beforeend`.
- `hx-trigger="every .1s"` is used to create an animation effect by requesting new rows periodically.





