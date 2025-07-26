# YACRUD
Yet Another CRUD

⚠This was written and debugged in a Linux environment with Python version 3.11.X.
Terminal environment supported 256 color and ANSI escape character codes.
Rich module is needed to run.
A requirements text file is included for those who need Python virtual environments.⚠

<img width="885" height="308" alt="image" src="https://github.com/user-attachments/assets/b6b907c7-756f-46d9-91c1-50a5f7520637" />

This was a small program I wrote for my Intro to Python class at FHSU. It solved a non-issue problem I have in my household:
Inventory management.
Why inventory management?
Because I have too much stuff.
Computer parts, computers, tablets, etc.
Even frozen food igredients.
While I might know where everything is, what I don't know, is how many things.
I built YACRUD for that reason. Because it's hard to keep count of things.

Now, I didn't stop there. I could have just left it at inventory management, but what about inventory *display?*
The "database" files are simple JSON files that can be pushed (via scp, rysnc, or whatever) over a local network to a Magic Mirror.
That's the niche I was filling for myself. Displaying food inventory would reduce the time my wife and I spend thinking about what to have for dinner, or making shopping lists.
Realistically, the time saved vs time invested ratio is off; I do have a program that I built myself, for myself.

This will, either in pieces or as a whole, serve as the backbone to other projects I have planned.
This includes, but is not limited to:
<ul>
  <li>A grocery store sales web scraper that calculates the unit price (if not provided) that saves as a JSON file type that I will push to my magic mirror to effortlessly hunt for the best sales.</li>
  <li>A personal movie database collection app that where you can track what movies you have, that can then recommend you movies from TMDB based on genre, runtime, actors/actresses/directors, etc and (possibly) show you sources that you can stream it from.</li>
</ul>
