## EDUTC

### Graphical schedule creator

The idea of the project is to process the emails :mailbox: that my university sends us to inform us of our schedule. In order to be better organized, I want to see it in a graphical form. :calendar:
In my university, there is already a website that allows us to do that : [Emploi d'UT temps](https://github.com/simde-utc/emploidutemps). 
However, when we receive the email, the website is ofen down because of the numbers of people.
So there is a problem and I need a solution to fix that ! What a better way to automate this process! :computer:

Consequently I decided to create a python script that will be able to transform this email into a schedule that can be viewed in png format.

For that, I use the PIL module of python which allows to create an image as well as the random and collections modules in order to process the message.

The mail format is :


![image](https://user-images.githubusercontent.com/86049841/233201994-8b81dae3-6728-4729-86d4-894619b44de3.png)


Finally, I get this graphical schedule (for example):

![image](https://user-images.githubusercontent.com/86049841/233202746-db89f2e0-8d93-47ab-abb9-f099cd76b0ca.png)

