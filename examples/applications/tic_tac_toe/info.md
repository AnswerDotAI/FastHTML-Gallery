# Tic Tac Toe Web App

This project is a web-based implementation of the classic Tic Tac Toe game built by Adedara Adeloro using FastHTML, HTMX, and Tailwind CSS.

The build steps from the original project were simplifed to use CDNs for the FastHTML Gallery version.  To check out the original project, click [here](https://github.com/TechBroAdedara/TicTacToe-with-FastHTML)

## Key Technologies and Techniques

1. **FastHTML**: A Python-based framework for building web applications with a focus web fundamentals
2. **HTMX**: HTMX is used to create the dynamic server-side content updates that lets you interact with the app without page reloads.
3. **Tailwind CSS**: Tailwind classes are used throughout the HTML to style the app, providing a clean and responsive design. For example `cls="grid grid-cols-3 grid-rows-3` creates a 3x3 grid for the Tic Tac Toe board. 

## How It Works

### Server-Side Logic

The app uses FastHTML to define routes and handle game logic on the server. Key routes include:

- `/`: The main page that renders the initial game board.
- `/on_click`: Handles player moves and updates the game state.
- `/restart`: Resets the game board.

### State Management

The game state is managed server-side using global variables:

- `button_states`: A 2D array storing snapshots of the board.
- `current_state_index`: Tracks the current state of the game.
- `winner_found_game_ended`: A flag to indicate if the game has ended.

### Dynamic Content

HTMX is used extensively to create a dynamic user interface

- `hx-get` attributes on buttons trigger GET server requests on click.
- `hx-target` specifies where the response from the server should be put.
- `hx-swap` determines how the new content should replace the old content.  In this app `outerHTML` is used to replace the entire element.