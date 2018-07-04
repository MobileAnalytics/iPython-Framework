//
//  main.m
//  spritybird
//
//  Created by Alexis Creuzot on 09/02/2014.
//  Copyright (c) 2014 Alexis Creuzot. All rights reserved.
//

#import <UIKit/UIKit.h>
#include "iPython_Framework.h"

int main(int argc, char * argv[])
{
    @autoreleasepool {
        return PyRunFile("main.py");
//        return PyRunString("print('Hello world!')");
    }
}
