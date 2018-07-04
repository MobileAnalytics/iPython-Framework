//
//  iPython_Framework.h
//  iPython Framework
//
//  Created by Administrator on 11/04/2018.
//  Copyright © 2018 pysas. All rights reserved.
//

#import <UIKit/UIKit.h>

//! Project version number for iPython_Framework.
FOUNDATION_EXPORT double iPython_FrameworkVersionNumber;

//! Project version string for iPython_Framework.
FOUNDATION_EXPORT const unsigned char iPython_FrameworkVersionString[];

// In this header, you should import all the public headers of your framework using statements like #import <iPython_Framework/PublicHeader.h>

int PyRunFile(const char *fileName);
int PyRunString(const char *code);
