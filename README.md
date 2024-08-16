***IF YOU CHOOSE TO ACTUALLY INSTALL THE GAME, I CREATED A SETUP FILE .EXE THAT ACTUALLY INSTALLS THE GAME***

This is my first ever game created in pygame. I created this project almost entirely from scratch. My only reference being the actual flappy bird game. The main file structure, sprites class, and ui class was done using a template of boiler plate code which I made to make 
it easier to make smaller game projects. The flappy bird, ground, pipe and all the number sprites were created by me. Only the icon which I used for compiling the program into my own installer, and the background sprite was found from the internet. All the sound effects 
were also created by me. At this point, I have been coding for around 6 months. Overall this project might've took 40 hours give or take.

I am aware that the sprites class is long. I had reused it from a previous project where I was testing how to automate the initialization of the sprites. It uses asprite and it's CLI (command line interface), which constructs a json file, as seen in the json folder, 
which then tells the sprite class information about the sprite sheet in order to declare it's areas rect values.

The check_collision function in the main file may not be the best way to go about it. I'm aware that pygame comes with many collision functions. Regardless, I wanted to figure it out for myself. 
