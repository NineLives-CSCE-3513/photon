# Photon
<p align="center">
   <img src="/assets/images/splash.jpg" width="100%" alt="Photon Logo">
</p>

Recreating the classic Photon laser tag system using modern technologies. This project was created for the Fall 2023 semester of the Software Engineering course at the University of Arkansas.

This branch is included to support Linux users by removing all sounds from the game. Installation instructions remain relatively the same as the main branch, with changes to the `requirements.txt` file.

## Download the Project
You may either download the project as a ZIP or clone the repository to your local machine:

```bash
$ git clone https://github.com/NineLives-CSCE-3513/photon.git
```

Open 2 terminal windows and navigate to the project directory in both:

```bash
$ cd /path/to/photon
```

Switch to the `linux-support` branch:

```bash
$ git checkout linux-support
```

Run the following to install the Tkinter library, which is required to run the program:

```bash
$ sudo apt-get install python3-tk
```

## Setting Up Supabase Credentials

You will need to create a [Supabase](https://supabase.com/) account. Create a new project with a table named `users`. Once you have created a new project, navigate to the project settings and copy the `Project URL` and `service_role` key from the `API` tab. You will need to set these as environment variables on your local machine. Included is a `.env.example` with the following contents:

```bash
SUPABASE_URL='your_url_here'
SUPABASE_KEY='your_key_here'
```

Rename the file to `.env` and replace the placeholder values with your Supabase project URL and service role key. The `.env` file is already included in the `.gitignore` file, so you don't have to worry about accidentally committing your credentials to version control.

## Running the Traffic Generator
Provided in the `src` directory is a file named `traffic_generator.py`. This file will generate UDP traffic to simulate the Photon laser tag units. In one of your terminal windows, run the following to start the traffic generator:

```bash
$ python src/traffic_generator.py
```

The program will prompt you to enter 2 equipment IDs for each team. We recommend using 10 and 20 for the green team and 30 and 40 for the red team.

## Running the Photon Program
A Makefile is provided to simplify running the main program. If you wish, you can run the program manually using the following commands:

```bash
$ pip install -r requirements.txt
$ python src/main.py
```

Alternatively, you can use the provided Makefile:

```bash
$ make
```

This will clean compiled bytecode files, install required dependencies, and run the main program. Run the following to display a menu of available commands:

```bash
$ make help
```

The player entry console will require using the `<tab>` key to switch between each field. When you've completed registering players for one team, use the mouse to select the other team's first equipment ID field and continue registering players. Click either the `Continue` button or press `<F5>` to finalize player registration and continue to the countdown screen. Press `<F12>` while still in the player entry console to clear all player entries.

Make sure that the equipment IDs you entered in the traffic generator match the ones you entered in the player entry console. To exit the program at any time, press the escape key or click the close button in the top right corner of the window.

## Screenshots:
<img src="https://github.com/NineLives-CSCE-3513/photon/assets/98860495/8116f404-ed5f-4314-9ec5-ddfed8dd7004" width="100%" />
<img src="https://github.com/NineLives-CSCE-3513/photon/assets/98860495/d50b8491-7db9-4558-a1be-204d32440324" width="100%" />
<img src="https://github.com/NineLives-CSCE-3513/photon/assets/98860495/c1aa6bf0-32d6-40f5-8b46-2cce0f39a661" width="100%" />

## Contributors:
<table>
   <thead>
      <tr>
            <th><p align="center">Name</p></th>
            <th><p align="center">GitHub Username</p></th>
      </tr>
   </thead>
   <tbody>
      <tr>
            <td><p align="center">Thomas Buser</p></td>
            <td><p align="center"><a href="https://github.com/tjbuser">tjbuser</a></p></td>
      </tr>
      <tr>
            <td><p align="center">Sophia Forrester</p></td>
            <td><p align="center"><a href="https://github.com/asophiaforrester">asophiaforrester</a></p></td>
      </tr>
      <tr>
            <td><p align="center">Grace Schmidt</p></td>
            <td><p align="center"><a href="https://github.com/GraceSchmidt1">GraceSchmidt1</a></p></td>
      </tr>
      <tr>
            <td><p align="center">Uyen Thi My Ho</p></td>
            <td><p align="center"><a href="https://github.com/uho2003">uho2003</a></p></td>
      </tr>
      <tr>
            <td><p align="center">Vishal Jeyam</p></td>
            <td><p align="center"><a href="https://github.com/vjeyam">vjeyam</a></p></td>
      </tr>
      <tr>
            <td><p align="center">Cade DuPont</p></td>
            <td><p align="center"><a href="https://github.com/cadedupont">cadedupont</a></p></td>
      </tr>
   </tbody>
</table>

## License
This project is licensed under the [MIT License](LICENSE).