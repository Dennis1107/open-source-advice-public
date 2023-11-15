# open-source-advice.com

<img src="logo.PNG" width=25% height=25%>

[Demo Video](https://drive.google.com/file/d/1M1CSJ8oPYBMl-HSZ6QERqF22ptQMsaKJ/view?usp=sharing)

# How it started
A couple of months have passed since my last personal project. I had a bit of time and high motivation to code again. The purpose of this project was not really to do a new side project but rather have fun coding something new and maybe this could evolve to something. 

# Problem
I came up with the idea to create a marketplace for open source contributors to offer their consulting service of their projects. For the open source projects this could help to monetize their project and attract other contributors. For the customers this could help to find highly skilled experts if they have specific questions of a particular open source project. 

# Solution
The experience of my previous one-on-one.tech project helped me a lot for setting up a first project structure and in particular the Django Backend. One thing which always disturbed me was the fact that usually each page needs a complete fresh render. I heard of [HTMX](https://htmx.org/) which helps in this case so that only a specific part of the frontend is rendered new. For the frontend is used [Tailwind](https://tailwindcss.com/) this time together with a little bit of [Alpine.js](https://alpinejs.dev/). 
One early decision was that even without registering as a user the offers should be visible which means there is no real landing page. I learned from my previous projects that the register process stops people from trying your product. As soon as you visit the main page you can directly see all offers and try the product in a limited way. As soon as you want to contact someone you have to create an account. This time the messaging was not included in the app but all works via email (postmark).

# Deployment
As Heroku started to cut of their starter packages I moved to [render](https://render.com/). The deployment process was very easy and super fast. I also really enjoyed the CI process which always deploys the application as soon as there is a git push on the main branch.
After all the fun things were ready (I enjoy the coding part way more than the distribution part) I reached out to some open source people and speaking with them. Very soon I realized that most of the people just don’t have time for consulting or have their own consulting already in place just within Github. I therefore decided to not further pursue this idea but it was still fun to code something again 😊

# Lessons Learned
This project helped me a lot to further deepen my knowledge in coding. I did a lot of things different to my first Django project which made it easier to make it right from the beginning. I honestly fall in love with HTMX because it makes it very easy to build more UI/UX friendly applications with Django.
Apart from that I learned (again) to first speak to users and really understand the underlying problem before building something. But this was clear to me from the beginning as I just wanted to be in the “creater modus” again.

