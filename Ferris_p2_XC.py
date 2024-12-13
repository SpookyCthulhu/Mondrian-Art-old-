"""
File : Project 2 Extra
Author: Michelle Ferris
Date: 12/12/19
Section: 0001
Email: michelle.ferris@maine.edu
Description: The Extra credit mondrian art project.

Sorry to anyone who has to read this... you don't have to read this right?
It just makes pretty pages, be satisfied with that.
"""


import random
import math

class div:
    # type of object, width, height, x position, y position, div identifier.
    def __init__(self, width, height, x, y, div):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.div = div

    # Checks what split, if nothing it turns the div into html, otherwise it splits into 2/4 new divs. pops on exit.
    def split(self, split, html):
        boxDimensions = []
        boxPositions = []
        # == True is unnecessary, "if True:" and "if False:" works by itself without "if True == True". You probably knew that, but I didn't.
        if split[0] == False and split[1] == False:
            global count
            count += 1
            self.div = "div" + str(count)
            return self.chooseTexture(html)
        if split[0]:
            splitVert = random.randrange(33, 67)
            oppWidth = int(self.width - self.width * (splitVert / 100))
            newWidth = self.width - oppWidth
            boxDimensions = [[newWidth, self.height], [oppWidth, self.height]]
            boxPositions = [[self.x, self.y], [self.x + newWidth, self.y]]
        if split[1]:
            splitHor = random.randrange(33, 67)
            oppHeight = int(self.height - self.height * (splitHor / 100))
            newHeight = self.height - oppHeight
            if len(boxDimensions) > 0:
                boxDimensions = [[newWidth, newHeight], [oppWidth, newHeight], [newWidth, oppHeight],
                                 [oppWidth, oppHeight]]
                boxPositions.append([self.x, self.y + newHeight])
                boxPositions.append([self.x + newWidth, self.y + newHeight])
            else:
                boxDimensions = [[self.width, newHeight], [self.width, oppHeight]]
                boxPositions = [[self.x, self.y], [self.x, self.y + newHeight]]
        # Creates an object for each pair of dimensions in boxDimensions
        for i in range(len(boxDimensions)):
        # appends a new object, with it's respective dimensions, x and y location, and new name)
            divList.append(div(boxDimensions[i][0], boxDimensions[i][1], boxPositions[i][0], boxPositions[i][1], "unfinished"))
        # Doesn't write anything if it split, we only write code for the final divs.
        return html

    # Determines whether this indivisible div is color or white texture.
    def chooseTexture(self, html):
        # Adust this stuff to tweak the ratio of color to textured cubes. You can also change the colors below.
        color = random.random()
        if color <= 0.25:
            self.type = color
            if color < 0.0833:
                color = "red"
            elif color < 0.1667:
                color = "royalblue"
            elif color < 0.25:
                color = "gold"
            # new property, just used to store a value without changing all the function calls.
            self.type = "color"
            self.color = color
            return self.addHtml(html)
        # replaces white with a pattern.
        else:
            self.type = "textured"
            return self.createTexture(html)

    # produces the initial texture object after determining the patterns the rest will follow.
    def createTexture(self, html):

        choices = [True, False]
        # specifies the domain of the function below.
        x = (random.random() * 2 - 1)
        y = random.random()
        if random.choice(choices) == True:
            # Checks between range x -1 and 1 on function.
            # Just a sigmoid with a steep slope around 0.
            variable1 = (1 / (1 + math.exp(-10 * x)))
            # inverse of the last function on range 0 to 1.
            variable2 = (1 / (1 + math.exp(10 * y)))
        else:
            variable2 = (1 / (1 + math.exp(-10 * x)))
            # inverse of the last function on range 0 to 1.
            variable1 = (1 / (1 + math.exp(10 * y)))


        # dimensions of the first rectangle that initiates the pattern.
        startW = 10 + int(self.width * variable1)
        startH = 10 + int(self.height * variable2)

        # x and y position on the canvas, if negative the overflow property hides portions, while carrying it's "ripples".
        # the /4 and /8 represent how much the start can escape the div, so that some cubes have ripples with no center.
        startX = random.randint(int(-(self.width / 4)), int(self.width) + int(self.width / 8))
        startY = random.randint(int(-(self.height / 4)), int(self.height) + int(self.width / 8))

        # will represent how to transform the left and top margins / width and height lengths.
        transform = [[], []]

        # Used to relate the buffer to the side length modification.

        # Amount to transform side lengths by.
        transform[0].append(random.randint(int(self.width / 8), int(self.width / 4)))
        transform[1].append(random.randint(int(self.height / 8), int(self.height / 4)))

        # Used to keep a minimum distance between the sides of each ripple. Buffer = 1/4th the transform size.
        bufferX = int(1 / 4 * transform[0][0])
        bufferY = int(1 / 4 * transform[1][0])

        # amount to add to the x and y translation for left and top.
        transform[0].append(random.randint(bufferX - transform[0][0], -bufferX))
        transform[1].append(random.randint(bufferY - transform[1][0], -bufferY))

        # creates div container for the ripple effect.
        html = self.addHtml(html)

        # Redefines the object to be type ripple, which is the texture inside a textured block.
        self.type = "ripple"
        self.oldWidth = self.width
        self.oldHeight = self.height
        self.oldX = self.x
        self.oldY = self.y
        self.Width = startW
        self.height = startH
        self.x = startX
        self.y = startY
        self.parent = self.div
        self.identifier = 1
        self.div = "ripple" + str(self.identifier) + "C" + str(count)
        self.index = 0
        # 50, 50 chance.
        if random.choice(choices):
            self.color = "black"
        else:
            self.color = "white"
        return self.rippleTexture(transform, html)

    # Takes in one square, makes a whole bunch with repeated transform properties applied.
    def rippleTexture(self, transform, html):
        # Base case is when a ripple has all of it's sides outside of viewable field.
        if self.oldX + self.x + self.width > self.oldX + self.oldWidth and self.oldX + self.x < self.oldX and \
        self.oldY + self.y + self.height > self.oldY + self.oldHeight and self.oldY + self.y < self.oldY:
            return html
        html = self.addHtml(html)

        if self.color == "black":
            self.color = "white"
        else:
            self.color ="black"
        self.width = self.width + transform[0][0]
        self.height = self.height + transform[1][0]
        self.x = self.x + transform[0][1]
        self.y = self.y + transform[1][1]
        self.identifier += 1
        self.div = "ripple" + str(self.identifier) + "C" + str(count)
        # negative z-index, doesn't make a difference.
        self.index = self.index - 1

        return self.rippleTexture(transform, html)


    # Splits some string and adds some code, for standardization and convenience.
    def injectCode(self, html, tag, code):
        left = html[:tag]
        right = html[tag:]
        html = left + code + right
        return html

    # Adds whatever code is specified by the input type to a string, which will be written to a document end.
    def addHtml(self, html):
        # creates body divs for everything but ripples.
        bodyCode = "<div id=" + self.div + ">\n</div>\n"
        if self.type == "ripple":
            bodyCode = "\t" + bodyCode[:-7] + "\t</div>\n"
        # shared code.
        styleCode = "#" + self.div + " {\n\twidth: " + str(self.width) + "px;\n\theight: " + str(self.height) + "px;\n\t" \
        "position: absolute;\n\tleft: " + str(self.x) + ";\n\ttop: " + str(self.y) + ";\n"
        if self.type == "color":
            styleCode += "\tbackground-color: " + self.color + ";\n\tborder: solid 5px black;\n"
        if self.type == "ripple":
            styleCode += "\tz-index: " + str(self.index) + ";\n\tbackground-color: " + self.color + ";\n"
        if self.type == "textured":
            styleCode += "\toverflow: hidden;\n\tborder: solid 5px black;\n"
        # adds closing bracket to either.
        styleCode += "}\n"

        styleMark = html.index("style") + (len("style") + 2)
        html = self.injectCode(html, styleMark, styleCode)
        bodyMark = html.index("body") + (len("body") + 2)
        if self.type == "ripple":
            bodyMark = html.index(self.parent, bodyMark) + len(self.parent) + 2
        html = self.injectCode(html, bodyMark, bodyCode)

        return html


# Basically main, it's the recursive part that determines whether to split.
def recursiveDivs(html, divList, minLength):
    # Base Case
    if len(divList) == 0:
        return html
    div = divList[0]
    # Determines which, if any, sides need to be split.
    splitVertical = False
    splitHorizontal = False
    if div.width > maxWidth/2:
        splitVertical = True
    else:
        try:
            check = random.randrange(minLength, int(div.width*1.5))
        except:
            check = minLength
        if check < div.width:
            splitVertical = True
    if div.height > maxHeight/2:
        splitHorizontal = True
    else:
        try:
            check = random.randrange(minLength, int(div.height*1.5))
        except:
            check = minLength
        if check < div.height:
            splitHorizontal = True
    # Splits the div into new divs based on which sides are to be split.
    html = div.split([splitVertical, splitHorizontal], html)
    # removes the div that was just finished.
    divList.pop(0)
    return recursiveDivs(html, divList, minLength)

def goldenRatio(html, divList, minLength):

    return goldenRatio(html, divList, minLength)

# represents the number of divs created at any given time, used for unique ID's.
html = "<html>\n<head></head>\n<style>\n</style>\n<body>\n</body>\n</html>"
count = 0
# Change these max numbers to get different sizes.
maxWidth = 1920
maxHeight = 1080
main = div(maxWidth, maxHeight, 0, 0, "main")
divList = [main]
# the 80 deteremines the minimum size of the cube, feel free to change it, but it will likely reach max recursion if lowered.
# Btw, 80 might break too, just infrequently. feel free to increase it.
html = recursiveDivs(html, divList, 80)
f = open("Project2Extra.html", "w+")
f.write(html)
f.close()