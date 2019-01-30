//
//  BE-oc.m
//  Parking
//
//  Created by Aditya Sriwasth on 4/25/18.
//  Copyright © 2018 Facebook. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(ViewController, NSObject)

//RCT_EXTERN_METHOD(Scan_bluetooth: (RCTResponseSenderBlock)callback);
RCT_EXTERN_METHOD(BloomEncrypt:(NSString*)message callback:(RCTResponseSenderBlock)callback);
RCT_EXTERN_METHOD(StartBLE:(RCTResponseSenderBlock)callback );
//RCT_EXTERN_METHOD(cancelScan: (RCTResponseSenderBlock)callback);
//RCT_EXTERN_METHOD(prints: (RCTResponseSenderBlock)callback);
@end
