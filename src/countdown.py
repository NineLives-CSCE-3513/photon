from typing import Dict
from PIL import Image, ImageTk
import cv2
import os
import tkinter as tk
import pygubu

from networking import Networking

# If on Windows, import winsound, else import playsound for countdown music
if os.name == "nt":
    import winsound
else:
    import playsound

def update_timer(timer_label: tk.Label, seconds: int, main_frame: tk.Frame, network: Networking, users: Dict, root: tk.Tk) -> None:
    # Update text being displayed in timer label
    timer_label.config(text=f"Game Starts In: {seconds} Seconds")

    # If there is still time left, recursively call this function after 1 second
    # Otherwise, destroy countdown frame and start game
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer, timer_label, seconds, main_frame, network, users, root)
    else:
        # Destroy main frame and start game, transmitting start game code
        main_frame.destroy()
        network.transmit_start_game_code()

        import play_action 
        play_action.build(network, users, root)

def update_video(video_label: tk.Label, cap: cv2.VideoCapture, frame_rate: int, video_width: int, video_height: int) -> None:
    # Read the next frame from the video, resize it, and convert it to PhotoImage for placing in the label
    # Recursively call this function after 1 / frame_rate seconds
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (video_width, video_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=photo)
        video_label.photo = photo
        video_label.after(1000 // frame_rate, update_video, video_label, cap, frame_rate, video_width, video_height)
    else:
        # Rewind the video to the beginning when it ends
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        update_video(video_label, cap, frame_rate, video_width, video_height)

def build(root: tk.Tk, users: Dict, network: Networking) -> None:
    # Load the UI file and create the builder
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("assets/ui/countdown.ui")

    # Based on OS, play the countdown sound
    # Play sound asynchronously to prevent freezing
    if os.name == "nt":
        winsound.PlaySound("assets/sounds/countdown.wav", winsound.SND_ASYNC)
    else:
        playsound.playsound("assets/sounds/countdown.wav", block=False)

    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # For each user entry, fill in username for each team
    for team in users:
        count: int = 1
        for user in users[team]:
            builder.get_object(f"{team}_username_{count}", main_frame).config(text=user.username)
            count += 1

    # Get the time frame and label from the UI file
    countdown_frame: tk.Frame = builder.get_object("countdown_frame", main_frame)
    video_frame: tk.Frame = builder.get_object("video_frame", countdown_frame)
    timer_label: tk.Label = builder.get_object("countdown_label", main_frame)

    # Make the video label and load video
    video_label: tk.Label = tk.Label(video_frame)
    video_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    cap: cv2.VideoCapture = cv2.VideoCapture("assets/videos/countdown.mp4")
    
    # Define video property variables, countdown length in seconds
    frame_rate: int = int(cap.get(cv2.CAP_PROP_FPS))
    video_width: int = 500
    video_height: int = 500
    seconds: int = 30

    # Start the countdown
    update_timer(timer_label, seconds, main_frame, network, users, root)

    # Start displaying the video
    update_video(video_label, cap, frame_rate, video_width, video_height)