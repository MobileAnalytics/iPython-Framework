from objc import *
from Quartz.CoreGraphics import CGRectMake, CGAffineTransformMakeScale
from _UIKit import UIApplicationMain
from Scene import *

#import classes
NSObject = lookUpClass("NSObject")
UIApplication = lookUpClass("UIApplication")
UIWindow = lookUpClass("UIWindow")
UIAlertController = lookUpClass("UIAlertController")
UIAlertAction = lookUpClass("UIAlertAction")
UIBarButtonItem = lookUpClass("UIBarButtonItem")
UIButton = lookUpClass("UIButton")
UIColor = lookUpClass("UIColor")
UIView = lookUpClass("UIView")
NSBundle = lookUpClass("NSBundle")
UITextField = lookUpClass("UITextField")
UINavigationController = lookUpClass("UINavigationController")
UIViewController = lookUpClass("UIViewController")
UIDevice = lookUpClass("UIDevice")
UITextView = lookUpClass("UITextView")
UIScreen = lookUpClass("UIScreen")
UIImage = lookUpClass("UIImage")
NSString = lookUpClass("NSString")
NSValue = lookUpClass("NSValue")
CABasicAnimation = lookUpClass("CABasicAnimation")
NSMutableArray = lookUpClass("NSMutableArray")
UIResponder = lookUpClass("UIResponder")

UIApplicationDelegate = objc._protocolNamed("UIApplicationDelegate")

r = objc.registerMetaDataForSelector
objc._updatingMetadata(True)
try:
    r(b'NSString', b'stringWithFormat:', {'arguments': {2: {'printf_format': True, 'type': '@'}}, 'variadic': True})
finally:
    objc._updatingMetadata(False)


rootVC = None

UIViewAnimationOptionCurveEaseIn               = 1 << 16

SceneDelegate = formal_protocol("SceneDelegate", None, (
                                                        objc.selector(None, selector=b"eventStart", signature=b"v@:"),
                                                        objc.selector(None, selector=b"eventPlay", signature=b"v@:"),
                                                        objc.selector(None, selector=b"eventWasted", signature=b"v@:")
                                                        ))

def viewAnimations():
    rootVC.gameOverView._.alpha = 0
    rootVC.gameOverView.setTransform_(CGAffineTransformMakeScale(0.8, 0.8))
    rootVC.flash._.alpha = 0
    rootVC.getReadyView._.alpha = 1

def viewCompletion(finished):
    rootVC.flash.removeFromSuperview()

def eventPlayanimations():
    rootVC.getReadyView._.alpha = 0

def eventWastedAnimations():
    #        // Display game over
    global rootVC
    rootVC.flash._.alpha = 0.4
    rootVC.gameOverView._.alpha = 1
    rootVC.gameOverView.setTransform_(CGAffineTransformMakeScale(1, 1))
        #        // Set medal
    if(rootVC.scene.score >= 40):
        rootVC.medalImageView._.image = UIImage.imageNamed_("medal_platinum")
    elif (rootVC.scene.score >= 30):
        rootVC.medalImageView._.image = UIImage.imageNamed_("medal_gold")
    elif (rootVC.scene.score >= 20):
        rootVC.medalImageView._.image = UIImage.imageNamed_("medal_silver")
    elif (rootVC.scene.score >= 10):
        rootVC.medalImageView._.image = UIImage.imageNamed_("medal_bronze")
    else:
        rootVC.medalImageView._.image = None
    #        // Set scores

    rootVC.currentScore._.text = '{}'.format(rootVC.scene.score)
    rootVC.bestScoreLabel._.text = '{}'.format(Score.bestScore())

def eventWastedcompletion(bFinished):
    rootVC.flash._.userInteractionEnabled = NO

objc.parseBridgeSupport('''\
    <?xml version='1.0'?>
    <!DOCTYPE signatures SYSTEM "file://localhost/System/Library/DTDs/BridgeSupport.dtd">
    <signatures version='1.0'>
    <class name='UIView'>
        <method selector='animateWithDuration:delay:options:animations:completion:'>
            <retval type='v'/>
            <arg index='0' block='false' type='d' />
            <arg index='1' block='false' type='d' />
            <arg index='2' block='false' type='Q' />
            <arg index='3' block='true' type='@?'>
                <retval type='v'/>
            </arg>
            <arg index='4' block='true' type='@?'>
                <retval type='v'/>
                <arg type='B' />
            </arg>
        </method>
        <method selector='animateWithDuration:animations:completion:'>
            <retval type='v'/>
            <arg index='0' block='false' type='d' />
            <arg index='1' block='true' type='@?'>
                <retval type='v'/>
            </arg>
            <arg index='2' block='true' type='@?'>
                <retval type='v'/>
                <arg type='B' />
            </arg>
        </method>
        <method selector='animateWithDuration:animations:'>
            <retval type='v'/>
            <arg index='0' block='false' type='d' />
            <arg index='1' block='true' type='@?'>
                <retval type='v'/>
            </arg>
        </method>
    </class>
    <class name='UIViewController'>
        <method selector='presentViewController:animated:completion:'>
            <retval type='v'/>
            <arg index='0' block='false' type='@' />
            <arg index='1' block='false' type='B' />
            <arg index='2' block='true' type='@?'>
                <retval type='v'/>
            </arg>
        </method>
    </class>
    <class name='UIAlertAction'>
        <method selector='actionWithTitle:style:handler:'>
            <retval type='v'/>
            <arg index='0' block='false' type='@' />
            <arg index='1' block='false' type='q' />
            <arg index='2' block='true' type='@?'>
                <retval type='v'/>
                <arg type='@' />
            </arg>
        </method>
    </class>
    </signatures>
    ''', globals(), None)

class ViewController(UIViewController, protocols=[SceneDelegate]):
    gameView = IBOutlet()
    getReadyView = IBOutlet()
    gameOverView = IBOutlet()
    medalImageView = IBOutlet()
    currentScore = IBOutlet()
    bestScoreLabel = IBOutlet()
    scene = None
    flash = None
    def init(self):
        return self

    def initWithNibName_bundle_(self, nibName, nibBundle):
        self = super(ViewController, self).initWithNibName_bundle_(nibName, nibBundle)
        return self

    def viewDidLoad(self):
        super(ViewController, self).viewDidLoad()
        self.viewWillLayoutSubviews()
        sharedApp = UIApplication.sharedApplication()
        sharedApp.setStatusBarHidden_withAnimation_(YES, 0)
        self.scene = Scene.sceneWithSize_(self._.view.bounds().size)
        self.scene._.scaleMode = 1
        self.scene.delegate = self
        #self.gameView._.showsFPS = YES
        global rootVC
        rootVC = self
        #//         Present the scene
        self.gameOverView._.alpha = 0
        self.gameOverView.setTransform_(CGAffineTransformMakeScale(0.9, 0.9))
        self.gameView.presentScene_(self.scene)

    def prefersStatusBarHidden(self):
        return YES

    def eventStart(self):
        UIView.animateWithDuration_animations_completion_(2, viewAnimations, viewCompletion)

    def eventPlay(self):
        UIView.animateWithDuration_animations_(5, eventPlayanimations)

    def eventWasted(self):
        self.flash = UIView.alloc().initWithFrame_(self._.view.frame())
        self.flash._.backgroundColor = UIColor.whiteColor()
        self.flash._.alpha = 0.9
        self.gameView.insertSubview_belowSubview_(self.flash, self.getReadyView)
        self.shakeFrame()
        UIView.animateWithDuration_delay_options_animations_completion_(0.6, 0, UIViewAnimationOptionCurveEaseIn, eventWastedAnimations, eventWastedcompletion)

    def shakeFrame(self):
        animation = CABasicAnimation.animationWithKeyPath_("position")
        animation.setDuration_(0.05)
        animation.setRepeatCount_(4)
        animation.setAutoreverses_(YES)
        animation.setFromValue_(NSValue.valueWithCGPoint_(CGPointMake(self._.view.center().x - 4, self._.view.center().y)))
        animation.setToValue_(NSValue.valueWithCGPoint_(CGPointMake(self._.view.center().x + 4, self._.view.center().y)))
        self._.view._.layer.addAnimation_forKey_(animation, "position")

class MyAppDelegate(UIResponder, protocols=[UIApplicationDelegate]):
    window = objc.object_property()
        
    @window.getter
    def window(self):
        return self._window
    
    @window.setter
    def window(self, v):
        self._window = v

    def application_willFinishLaunchingWithOptions_(self, application, launchOptions):
        return YES

UIApplicationMain("MyAppDelegate")






