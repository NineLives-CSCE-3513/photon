import pygubu
import tkinter as tk
import os 
import random
import threading
from typing import Dict

from networking import Networking
from game_logic import GameState

# If on Windows, import winsound, else import playsound for countdown music
if os.name == "nt":
    import winsound
else:
    import playsound

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/play_action.ui")

def update_stream(game: GameState, action_stream: tk.Frame) -> None:
    # Add scroll effect to action stream with game.game_event_list queue
    if len(game.game_event_list) > 0:
        # Create new label for next event
        new_event: tk.Label = tk.Label(action_stream, text=str(game.game_event_list.pop()), font=("Fixedsys", 16), bg="#FFFFFF")
        new_event.pack(side=tk.TOP, fill=tk.X)
        
        # Remove the last event from the bottom of the action stream
        if len(action_stream.winfo_children()) > 5:
            action_stream.winfo_children()[0].destroy()

    # Recursively call this function after 1 second to incrementally update action stream
    action_stream.after(1000, update_stream, game, action_stream)

def update_score(game: GameState, main_frame: tk.Frame) -> None:
    # Update scores for green team
    for user in game.green_users:
        builder.get_object(f"green_username_{user.row}", main_frame).config(text=user.username)
        builder.get_object(f"green_score_{user.row}", main_frame).config(text=user.game_score)
    builder.get_object("green_total_score", main_frame).config(text=game.green_team_score)

    # Update scores for red team
    for user in game.red_users:
        builder.get_object(f"red_username_{user.row}", main_frame).config(text=user.username)
        builder.get_object(f"red_score_{user.row}", main_frame).config(text=user.game_score)
    builder.get_object("red_total_score", main_frame).config(text=game.red_team_score)

    # Recursively call this function after 1 second to incrementally update scores
    main_frame.after(1000, update_score, game, main_frame)

# Implementing play countdown timer for 6-minutes 
def update_timer(main_frame: tk.Frame, timer_label: tk.Label, seconds: int) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_label.config(text=f"Time Remaining: {mins:01d}:{secs:02d}")

    # Continue counting down, destroy main frame when timer reaches 0
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer, main_frame, timer_label, seconds)
    else:
        main_frame.destroy()

def build(network: Networking, users: Dict, root: tk.Tk) -> None:
    # Select random game music file
    file = random.choice(os.listdir("res/moosic"))

    # Based on OS, play the game music
    # Play sound asynchronously to prevent freezing
    if os.name == "nt":
        winsound.PlaySound("res/moosic/" + file, winsound.SND_ASYNC)
    else:
        playsound.playsound("res/moosic/" + file, block=False)

     # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timer_label: tk.Label = builder.get_object("countdown_label", main_frame)

    # Get action frame and prevent from resizing to fit label contents
    action_stream: tk.Frame = builder.get_object("action_stream_frame", main_frame)
    action_stream.pack_propagate(False)

    # Create game state model
    game: GameState = GameState(users)

    # Update score labels, timer, and action stream
    update_score(game, main_frame)
    update_stream(game, action_stream)
    update_timer(main_frame, timer_label, seconds=360)

    # Start thread for UDP listening
    game_thread: threading.Thread = threading.Thread(target=network.run_game, args=(game,))
    game_thread.start()
    # game_thread.join()