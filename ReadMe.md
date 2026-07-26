This branch is to avoid most of my rookie mistakes on the main branch as I was learning python. I'm still learning but you get the point.

# What is PatoDuck

Patoduck is an agnostic CMS for multi-language translation.

While translating my game, I've found myself over and over translating the same names, or breaking tags, one language not calling a function template right, having trouble with csv files not formatting text well or grammar check on libre office being angry I'm using two languages on the same file.

Translating files like this is not impossible. But every little distraction or mistake can break in production and go unnoticed, and that was with me, who spoke two actual Languages, writing it.

It doesn't scale well.

So I built a little tool that can either take care of all those little details, and that can be built upon on things that can annoy me.

For example, I don't see the *need* yet to see that one language references one variable or one function while the other doesn't, but I can create warnings for it.


# The Hyper Sassy BulmaX Unchained Stack

Welcome to your non-programmer weaaboo stack.

### Why Django?

Not my first choice, originally I was gonna go with good old PHP, and then the amount of boilerplate on Symphony for a simple MVC made me want to slap whoever thought that was good idea.

The same concept on Python's Django was, if I recall, 90 lines of code less.

It was an easy choice for someone who had to make a simple database and just keep things organized.

### Why Sass?

Because it is amazing. It is CSS without most of its bullshit syntax. Especially good when you don't need it as much.

### Why Bulma?

Because I love dragon ball, I used to fight Bootstrap's CSS with an army of !Important, and BeerCSS was mad at me.

Also future-proofed by being Sass compatible if I need to give up the cdn to something more complex.

### Why are you also using PicoCSS if you're using Bulma?

PicoCSS is the best prototyping library ever, and Bulma is so agnostic it will require classes even for headers.

I'm not interested on making the project pretty, just not messy, so having PicoCSS makes me create any page without thinking about classes, and when I have to do I still don't have to think about the ones I left missing.

Also future-proofed by being Sass compatible if I need to give up the cdn to something more complex.

### Why HTMX?

Because it is how simple server communication should be done. Validation on the back end, simply receive a string through HTTP request.

No fancy objects, no major lines of javascript, just the server.

### Is that god damn Hyperscript?

I am not a programmer.

I cannot stress enough how much I hate trying to read Javascript and its {()({}{}(););} syntax to something simple.

Hyperscript is a terrible scripting language where "to" and "from" will make you hate even trying to use a computer. But it is wonderful to just read a single line and understand.

I don't love hyperscript, I just hate javascript more.