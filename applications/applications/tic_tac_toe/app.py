from fasthtml.common import (
    fast_app,
    Div,
    H1,
    P,
    Button,
    Link,
    Script,
    Style,
)

style = Style(
    """
            body{
                min-height: 100vh;
                margin:0;
                background-color: #1A1A1E;
                display:grid;

            
            }"""
) # custom style to be applied globally.

hdrs = ( Script(src="https://cdn.tailwindcss.com") ,
        Script(src="https://unpkg.com/htmx.org@2.0.1", integrity="sha384-QWGpdj554B4ETpJJC9z+ZHJcA/i59TyjxEPXiiUgN2WmTyV5OEZWCD6gQhgkdpB/", crossorigin="anonymous"),
        Link(rel="stylesheet", href="/applications/applications/tic_tac_toe/output.css"),

        )
app, rt = fast_app(
    hdrs=(hdrs, style),
    pico=False,
    # live=True,
)

current_state_index = -1 #Used to navigate the current snapshot of the board
button_states = [[None for _ in range(9)] for _ in range(9)] #2D array to store snapshots of board
win_states = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
] #possible win streaks/states for Xs and Os

winner_found_game_ended = False

def check_win(player) -> bool:
    global button_states, current_state_index, winner_found_game_ended
    """This function checks if there's a win streak present in the board. Uses the win states list to check 
        If text at all text indices are equal and its not the placeholder text ("."), change the global variable "winner_found_game_ended" to True
    """
    for cell_1, cell_2, cell_3 in win_states:
        if (
            button_states[current_state_index][cell_1] != None
            and button_states[current_state_index][cell_1]
            == button_states[current_state_index][cell_2]
            and button_states[current_state_index][cell_2]
            == button_states[current_state_index][cell_3]
        ):
            winner_found_game_ended = True
            return f"Player {player} wins the game!"
        
    if all(value is not None for value in button_states[current_state_index]): 
        #if the current snapshot of the board doesn't have any placeholder text and there is no winning streak
        winner_found_game_ended = True
        return "No Winner :("
    
    return f'''Player {'X' if player == 'O' else 'O'}'s turn!'''
    #will keep returning this value [because its called after every button click], until a winner or none is found


def handle_click(index: int):
    """This function handles what text gets sent to the button's face depending on whose turn it is
    uses a weird algorithm"""
    global button_states, current_state_index
    next_index = current_state_index + 1
    button_states[next_index] = button_states[current_state_index][:] #make a copy of the current snapshot to add to the next snapshot

    if button_states[current_state_index][index] is None:
        if "X" not in button_states[current_state_index] or button_states[
            current_state_index
        ].count("X") <= button_states[current_state_index].count("O"):
            button_states[next_index][index] = "X"
        else:
            button_states[next_index][index] = "O"
    #ic(button_states)
    current_state_index += 1 
    return button_states[next_index][index]



@app.get("/on_click")  # On click, call helper function to alternate between X and O
def render_button(index:int):
    global button_states, current_state_index
    
    player = handle_click(index)
    winner = check_win(player)  # function that checks if there's a winner

    buttons = [ Button(
            f'''{text if text is not None else '.' }''', 
            cls="tic-button-disabled" if (text is not None) or winner_found_game_ended else "tic-button",
            hx_get=f"/applications/tic_tac_toe/app/on_click?index={idx}",
            disabled=True if (text is not None) or winner_found_game_ended else False,
            hx_target=".buttons-div",
            hx_swap='outerHTML'
        )
        for idx, text in enumerate(button_states[current_state_index]) 
        
    ]
    """rerenders buttons based on the next snapshot.
            I initially made this to render only the button that gets clicked. 
            But to be able to check the winner and stop the game, I have to use the next snapshot instead
            if you wanna see the previous implementation, it should be in one of the commits.
            """
    board = Div(
                Div(winner, cls="justify-self-center"),
                Div(*buttons, cls="grid grid-cols-3 grid-rows-3"),
                cls="buttons-div font-bevan text-white font-light grid justify-center"
            )
    return board


# Rerenders the board if the restart button is clicked.
# Also responsible for initial rendering of board when webpage is reloaded
@app.get("/restart")
def render_board():
    global button_states, current_state_index, winner_found_game_ended

    current_state_index = -1
    button_states = [[None for _ in range(9)] for _ in range(9)]
    winner_found_game_ended = False

    # button component
    buttons = [
        Button(
            ".",
            cls="tic-button",
            hx_get=f"/applications/tic_tac_toe/app/on_click?index={i}",
            hx_swap="outerHTML",
            hx_target=".buttons-div",
        )
        for i, _ in enumerate(button_states[current_state_index])
    ]
    return  Div(Div("Player X starts the game",cls="font-bevan text-white justify-self-center"),
                Div(*buttons, cls="grid grid-cols-3 grid-rows-3"),
                cls="buttons-div grid"
            )


# ---------------------------------------------Main Page --------------------------------------------
@app.get("/")
def homepage():
    global button_states
    return Div(
        Div(
            H1("Tic Tac Toe!", cls="font-bevan text-5xl text-white"),
            P(
                "A FastHTML app by Adedara Adeloro",
                cls="font-bevan text-custom-blue font-light",
            ),
            cls="m-14"
        ),
        Div(
            render_board(),  # render buttons.

            Div(
                # Button("Go to state 1", 
                #        cls="text-disabled-blue rounded-xl p-2 w-auto h-auto border-disabled-blue bg-custom-gray font-bevan text-xl m-3", 
                #        disabled=True,
                #        hx_get="/restart?state=4",
                #        hx_target=".buttons-div"),
                Button(
                    "Restart!",
                    cls="restart-button",
                    hx_get="/applications/tic_tac_toe/app/restart",
                    hx_target=".buttons-div",
                    hx_swap="outerHTML",
                    disabled=False,
                ),
                cls="flex flex-col items-center justify-center m-10",
            ),
            cls="flex flex-col items-center justify-center",
        ),
        cls="justify-center items-center h-screen bg-custom-background",
    )
