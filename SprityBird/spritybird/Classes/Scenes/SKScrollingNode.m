//
//  SKScrollingNode.m
//  spritybird
//
//  Created by Alexis Creuzot on 09/02/2014.
//  Copyright (c) 2014 Alexis Creuzot. All rights reserved.
//

#import "SKScrollingNode.h"

@implementation SKScrollingNode


+ (id) scrollingNodeWithImageNamed:(NSString *)name inContainerWidth:(float) width
{
    UIImage * image = [UIImage imageNamed:name];
    
    SKScrollingNode * realNode = [SKScrollingNode spriteNodeWithColor:[UIColor clearColor] size:CGSizeMake(width, image.size.height)];
    realNode.scrollingSpeed = 1;
    
    float total = 0;
    while(total<(width + image.size.width)){
        SKSpriteNode * child = [SKSpriteNode spriteNodeWithImageNamed:name ];
        [child setAnchorPoint:CGPointZero];
        [child setPosition:CGPointMake(total, 0)];
        [realNode addChild:child];
        total+=child.size.width;
    }
    
    return realNode;
}


- (void) update:(NSTimeInterval)currentTime
{
    [self.children enumerateObjectsUsingBlock:^(id child, NSUInteger idx, BOOL *stop){
//        ((SKSpriteNode *)child).position = CGPointMake(((SKSpriteNode *)child).position.x-self.scrollingSpeed, ((SKSpriteNode *)child).position.y);
        ((SKSpriteNode *)child).position = CGPointMake(((SKSpriteNode *)child).position.x-((SKScrollingNode *)((SKSpriteNode *)child).parent).scrollingSpeed, ((SKSpriteNode *)child).position.y);
        if (((SKSpriteNode *)child).position.x <= -((SKSpriteNode *)child).size.width){
            float delta = ((SKSpriteNode *)child).position.x+((SKSpriteNode *)child).size.width;
            ((SKSpriteNode *)child).position = CGPointMake(((SKSpriteNode *)child).size.width*(((SKScrollingNode *)((SKSpriteNode *)child).parent).children.count-1)+delta, ((SKSpriteNode *)child).position.y);
        }
    } ];
}

@end
