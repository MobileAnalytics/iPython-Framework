from objc import *
from Quartz.CoreGraphics import CGRectMake, CGSizeMake, CGPointZero, CGPointMake, CGVectorMake, CGRectGetMidY, CGRectGetMidX
from math import ceil
from Math import *

UIColor = lookUpClass("UIColor")
UIImage = lookUpClass("UIImage")
NSMutableArray = lookUpClass("NSMutableArray")
SKScene = lookUpClass("SKScene")
SKSpriteNode = lookUpClass("SKSpriteNode")
SKPhysicsContactDelegate = objc._protocolNamed("SKPhysicsContactDelegate")
SKTexture = lookUpClass("SKTexture")
SKAction = lookUpClass("SKAction")
SKLabelNode = lookUpClass("SKLabelNode")
SKPhysicsBody = lookUpClass("SKPhysicsBody")
NSUserDefaults = lookUpClass("NSUserDefaults")

M_PI = 3.14159265358979323846264338327950288
SKTextureFilteringNearest = 0
kBestScoreKey = "BestScore"

class Score(NSObject):
    @classmethod
    def bestScore(self):
        return NSUserDefaults.standardUserDefaults().integerForKey_(kBestScoreKey)

    @classmethod
    def setBestScore_(self, bestScore):
        NSUserDefaults.standardUserDefaults().setInteger_forKey_(bestScore, kBestScoreKey)
        NSUserDefaults.standardUserDefaults().synchronize()

    @classmethod
    def registerScore_(self, score):
        if(score > self.bestScore()) :
            self.setBestScore_(score)

def updateBlock(child, idx, stop):
    child.setPosition_(CGPointMake(child.position().x - child._.parent.scrollingSpeed, child.position().y))
    if(child.position().x <= (-child.size().width)):
        delta = child.position().x + child.size().width
        child.setPosition_(CGPointMake(child.size().width * (child._.parent._.children.count()-1) + delta, child.position().y))

#register the NSArray:enumerateObjectsUsingBlock: method to use block argument
parseBridgeSupport('''\
    <?xml version='1.0'?>
    <!DOCTYPE signatures SYSTEM "file://localhost/System/Library/DTDs/BridgeSupport.dtd">
    <signatures version='1.0'>
    <class name='NSArray'>
        <method selector='enumerateObjectsUsingBlock:'>
            <retval type='v'/>
            <arg index='0' block='true' type='@?'>
                <retval type='v'/>
                <arg type='@' />
                <arg type='Q' />
                <arg type='^B' />
            </arg>
        </method>
    </class>
    </signatures>
    ''', globals(), None)


class SKScrollingNode(SKSpriteNode):
    scrollingSpeed = None
    def scrollingNodeWithImageNamed_inContainerWidth_(self, name, width):
        image = UIImage.imageNamed_(name)
        imagewidth = image.size().width
        realNode = SKScrollingNode.spriteNodeWithColor_size_(UIColor.clearColor(), CGSizeMake(width, image.size().height))
        realNode.scrollingSpeed = 1
        total = 0

        while(total<(width + imagewidth)):
            child = SKSpriteNode.spriteNodeWithImageNamed_(name)
            child.setAnchorPoint_(CGPointZero)
            child.setPosition_(CGPointMake(total, 0))
            realNode.addChild_(child)
            total+=child.size().width

        return realNode


    def update_(self, currentTime):
        self._.children.enumerateObjectsUsingBlock_(updateBlock)


VERTICAL_SPEED = 1
VERTICAL_DELTA = 5.0
class BirdNode(SKSpriteNode):
    flap = None
    flapForever = None
    deltaPosY = 0
    goingUp = False

    def init(self):
        self = super(SKSpriteNode, self).init()
        birdTexture1 = SKTexture.textureWithImageNamed_("bird_1")
        birdTexture1._.filteringMode = SKTextureFilteringNearest
        birdTexture2 = SKTexture.textureWithImageNamed_("bird_2")
        birdTexture2._.filteringMode = SKTextureFilteringNearest
        birdTexture3 = SKTexture.textureWithImageNamed_("bird_3")
        birdTexture3._.filteringMode = SKTextureFilteringNearest
        self = BirdNode.spriteNodeWithTexture_(birdTexture1)
        self.flap = SKAction.animateWithTextures_timePerFrame_([birdTexture1, birdTexture2, birdTexture3], 0.2)
        self.flapForever = SKAction.repeatActionForever_(self.flap)

        self.setTexture_(birdTexture1)
        self.runAction_withKey_(self.flapForever, "flapForever")

        return self

    def update_(self, currentTime):
        if(self._.physicsBody is None):
            if(self.deltaPosY > VERTICAL_DELTA):
                self.goingUp = False

            if(self.deltaPosY < -VERTICAL_DELTA):
                self.goingUp = True

            if(self.goingUp):
                displacement = VERTICAL_SPEED
            else:
                displacement = -VERTICAL_SPEED;

            self.setPosition_(CGPointMake(self.position().x, self.position().y + displacement))
            self.deltaPosY += displacement

        if(self._.physicsBody is not None):
            self._.zRotation = M_PI * self._.physicsBody.velocity().dy * 0.0005
        else:
            self._.zRotation = 0


    def startPlaying(self):
        deltaPosY = 0
        self._.physicsBody = SKPhysicsBody.bodyWithRectangleOfSize_(CGSizeMake(26, 18))
        self._.physicsBody._.categoryBitMask = birdBitMask
        self._.physicsBody._.mass = 0.1
        self.removeActionForKey_("flapForever")

    def bounce(self):
        self._.physicsBody.setVelocity_(CGVectorMake(0, 0))
        self._.physicsBody.applyImpulse_(CGVectorMake(0, 40))
        self.runAction_(self.flap)

#Scene class
BACK_SCROLLING_SPEED = 0.5
FLOOR_SCROLLING_SPEED = 3

VERTICAL_GAP_SIZE = 120
FIRST_OBSTACLE_PADDING = 100
OBSTACLE_MIN_HEIGHT = 60
OBSTACLE_INTERVAL_SPACE = 130

backBitMask     =  1
birdBitMask     =  2
floorBitMask    =  4
blockBitMask    =  8

def WIDTH(scene):
    return scene.frame().size.width

def HEIGHT(scene):
    return scene.frame().size.height

def X(view):
    return view.frame().origin.x

def Y(view):
    return view.frame().origin.y

def LEFT(view):
    return view.frame().origin.x

def TOP(view):
    return view.frame().origin.y

def BOTTOM(view):
    return (view.frame().origin.y + view.frame().size.height)

def RIGHT(view):
    return (view.frame().origin.x + view.frame().size.width)

class Scene(SKScene, protocols=[SKPhysicsContactDelegate]):
    delegate = None
    score = 0
    wasted = False
    floor = None
    back = None
    scoreLabel = None
    bird = None
    nbObstackes = 0
    topPipes = None
    bottomPipes = None

    def initWithSize_(self, size):
        self = super(Scene, self).initWithSize_(size)
        if(self):
            self._.physicsWorld._.contactDelegate = self
            self.startGame()
        return self

    def startGame(self):
        self.wasted = False
        self.removeAllChildren()
        self.createBackground()
        self.createFloor()
        self.createScore()
        self.createObstacles()
        self.createBird()
#        // Floor needs to be in front of tubes
        self.floor._.zPosition = self.bird.zPosition() + 1;
        if(self.delegate is not None):
            self.delegate.eventStart()

    def createBackground(self):
        self.back = SKScrollingNode.scrollingNodeWithImageNamed_inContainerWidth_(self, "back", self.frame().size.width)
        self.back.scrollingSpeed = BACK_SCROLLING_SPEED
        self.back.setAnchorPoint_(CGPointZero)
        self.back._.physicsBody = SKPhysicsBody.bodyWithEdgeLoopFromRect_(self.frame())
        self.back._.physicsBody._.categoryBitMask = backBitMask
        self.back._.physicsBody._.contactTestBitMask = birdBitMask
        self.addChild_(self.back)


    def createScore(self):
        self.score = 0
        self.scoreLabel = SKLabelNode.labelNodeWithFontNamed_("Helvetica-Bold")
        self.scoreLabel._.text = "0"
        self.scoreLabel._.fontSize = 500
        self.scoreLabel.setPosition_( CGPointMake(CGRectGetMidX(self.frame()), 100))
        self.scoreLabel._.alpha = 0.2
        self.addChild_(self.scoreLabel)

    def createFloor(self):
        self.floor = SKScrollingNode.scrollingNodeWithImageNamed_inContainerWidth_(self, "floor", self.frame().size.width)
        self.floor.scrollingSpeed = FLOOR_SCROLLING_SPEED
        self.floor.setAnchorPoint_(CGPointZero)
        self.floor.setName_("floor")
        self.floor._.physicsBody = SKPhysicsBody.bodyWithEdgeLoopFromRect_(self.floor.frame())
        self.floor._.physicsBody._.categoryBitMask = floorBitMask
        self.floor._.physicsBody._.contactTestBitMask = birdBitMask
        self.addChild_(self.floor)

    def createBird(self):
        self.bird = BirdNode.alloc().init()
        self.bird.setPosition_(CGPointMake(100, CGRectGetMidY(self.frame())))
        self.bird.setName_("bird")
        self.addChild_(self.bird)

    def createObstacles(self):
#    // Calculate how many obstacles we need, the less the better
        mywidth = self.frame().size.width
        self.nbObstacles = ceil(mywidth/(OBSTACLE_INTERVAL_SPACE))
        lastBlockPos = 0
        self.bottomPipes = NSMutableArray.alloc().init()
        self.topPipes = NSMutableArray.alloc().init()

        for i in range(self.nbObstacles):
            topPipe = SKSpriteNode.spriteNodeWithImageNamed_("pipe_top")
            topPipe.setAnchorPoint_(CGPointZero)
            self.addChild_(topPipe)
            self.topPipes.addObject_(topPipe)
            bottomPipe = SKSpriteNode.spriteNodeWithImageNamed_("pipe_bottom")
            bottomPipe.setAnchorPoint_(CGPointZero)
            self.addChild_(bottomPipe)
            self.bottomPipes.addObject_(bottomPipe)
#            // Give some time to the player before first obstacle
            if(0 == i):
                self.place_and_atX_(bottomPipe, topPipe, mywidth+FIRST_OBSTACLE_PADDING)
            else:
                self.place_and_atX_(bottomPipe, topPipe, lastBlockPos + bottomPipe.frame().size.width +OBSTACLE_INTERVAL_SPACE)
            lastBlockPos = topPipe.position().x

    def touchesBegan_withEvent_(self, touches, event):
        if(self.wasted):
            self.startGame()
        else:
            if (self.bird._.physicsBody is None) :
                self.bird.startPlaying()
                if(self.delegate):
                    self.delegate.eventPlay()

            self.bird.bounce()

    def update_(self, currentTime):
        if(self.wasted) :
            return
#       // ScrollingNodes
        self.back.update_(currentTime)
        self.floor.update_(currentTime)

#        // Other
        self.bird.update_(currentTime)
        self.updateObstacles_(currentTime)
        self.updateScore_(currentTime)

    def updateObstacles_(self, currentTime):
        if(self.bird._.physicsBody is None):
            return

        for i in range(self.nbObstacles):
#        // Get pipes bby pairs
            topPipe = self.topPipes[i]
            bottomPipe = self.bottomPipes[i]
#        // Check if pair has exited screen, and place them upfront again
            if (X(topPipe) < -WIDTH(topPipe)):
                mostRightPipe = self.topPipes[(i+(self.nbObstacles-1))%self.nbObstacles]
                self.place_and_atX_(bottomPipe, topPipe, X(mostRightPipe)+WIDTH(topPipe)+OBSTACLE_INTERVAL_SPACE)
    #        // Move according to the scrolling speed
            topPipe.setPosition_(CGPointMake(X(topPipe) - FLOOR_SCROLLING_SPEED, Y(topPipe)))
            bottomPipe.setPosition_(CGPointMake(X(bottomPipe) - FLOOR_SCROLLING_SPEED, Y(bottomPipe)))

    def place_and_atX_(self, bottomPipe, topPipe, xPos):
#    // Maths
        myheight = self.frame().size.height
        floorheight = self.floor.frame().size.height
        availableSpace = myheight - floorheight
        maxVariance = availableSpace - (2*OBSTACLE_MIN_HEIGHT) - VERTICAL_GAP_SIZE
        variance = Math.randomFloatBetween_and_(self, 0, maxVariance)
        #print("--availableSpace--maxVariance--variance--", availableSpace, maxVariance, variance)
#        // Bottom pipe placement
        minBottomPosY = floorheight + OBSTACLE_MIN_HEIGHT - myheight
        bottomPosY = minBottomPosY + variance
        bottomPipe.setPosition_(CGPointMake(xPos,bottomPosY))
        bottomPipe._.physicsBody = SKPhysicsBody.bodyWithEdgeLoopFromRect_(CGRectMake(0,0, bottomPipe.frame().size.width , bottomPipe.frame().size.height))

        bottomPipe._.physicsBody._.categoryBitMask = blockBitMask
        bottomPipe._.physicsBody._.contactTestBitMask = birdBitMask

#        // Top pipe placement
        topPipe.setPosition_(CGPointMake(xPos,bottomPosY + bottomPipe.frame().size.height + VERTICAL_GAP_SIZE))
        topPipe._.physicsBody = SKPhysicsBody.bodyWithEdgeLoopFromRect_(CGRectMake(0,0, topPipe.frame().size.width, topPipe.frame().size.height))

        topPipe._.physicsBody._.categoryBitMask = blockBitMask
        topPipe._.physicsBody._.contactTestBitMask = birdBitMask

    def updateScore_(self, currentTime) :
        for i in range(self.nbObstacles) :
            topPipe = self.topPipes.objectAtIndex_(i)
            if(((X(topPipe) + WIDTH(topPipe)/2) > self.bird.position().x) and
               (X(topPipe) + WIDTH(topPipe)/2) < (self.bird.position().x + FLOOR_SCROLLING_SPEED)):
                self.score = self.score + 1
                self.scoreLabel._.text = '{}'.format(self.score)
                if(self.score>=10):
                    self.scoreLabel._.fontSize = 340
                    self.scoreLabel.setPosition_(CGPointMake(CGRectGetMidX(self.frame()), 120))

    def didBeginContact_(self, contact) :
        if(self.wasted):
            return

        self.wasted = True
        Score.registerScore_(self.score)
        if(self.delegate is not None):
            self.delegate.eventWasted()

#    def didEndContact_(self, contact) :
#        pass


