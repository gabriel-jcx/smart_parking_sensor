//
//  File.swift
//  Parking
//
//  Created by on 4/25/18.
//  Copyright © 2018 Facebook. All rights reserved.
//

import Foundation
import UIKit
import CoreBluetooth
//import CryptoSwift

//Uart Service uuid


let kBLEService_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
let kBLE_Characteristic_uuid_Tx = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
let kBLE_Characteristic_uuid_Rx = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
let MaxCharacters = 20

let BLEService_UUID = CBUUID(string: kBLEService_UUID)
let BLE_Characteristic_uuid_Tx = CBUUID(string: kBLE_Characteristic_uuid_Tx)//(Property = Write without response)
let BLE_Characteristic_uuid_Rx = CBUUID(string: kBLE_Characteristic_uuid_Rx)// (Property = Read/Notify)
var txCharacteristic : CBCharacteristic?
var rxCharacteristic : CBCharacteristic?
var blePeripheral : CBPeripheral?
var characteristicASCIIValue = NSString()
var AppPrivateKey = "React Native Sucks"
var ble_devices = [[String: Any]]()
var Power = [[String:Any]]()
var ble_names:[String] = []
var ble_dev: [String: Any]=["names": String.self];
@objc(ViewController)


class ViewController : UIViewController, CBCentralManagerDelegate, CBPeripheralDelegate{
  
  
  //Data
  
  
  var centralManager : CBCentralManager!
  var RSSIs = [NSNumber]()
  
  var data = NSMutableData()
  var writeData: String = ""
  var peripherals: [CBPeripheral] = []
  var characteristicValue = [CBUUID: NSData]()
  var timer = Timer()
  var characteristics = [String : CBCharacteristic]()
  //@objc func bloom_programming_phase(_ message:String, callback: @escaping RCTResponseSenderBlock){
  //  print(message)
 //   let password: Array<UInt8> = Array(message.utf8)
  //  let salt: Array<UInt8> = Array("2".utf8)
    /*do{
      let key = try PKCS5.PBKDF2(password: password, salt: salt, iterations: 4096, variant:.sha256).calculate()
      print(key)
      print(type(of: key))

    } catch{
      print("Error")
    }*/
  //}
  @objc func StartBLE(_ callback: @escaping RCTResponseSenderBlock){
    centralManager = CBCentralManager(delegate: self, queue: nil)
    DispatchQueue.main.asyncAfter(deadline: .now()+5.5, execute:{
      print(ble_devices)
      //print(ble_dev)
      callback([NSNull(),ble_devices,Power])
    })
    //convert peripheral to string array
    //return self.periherals
  }
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    centralManager = CBCentralManager(delegate: self, queue: nil)
  }
  
  override func viewDidAppear(_ animated: Bool) {
    disconnectFromDevice()
    super.viewDidAppear(animated)
    print("View Cleared")
  }
  
  override func viewWillDisappear(_ animated: Bool) {
    super.viewWillDisappear(animated)
    print("Stop Scanning")
    centralManager?.stopScan()
  }
  
  /*Okay, now that we have our CBCentalManager up and running, it's time to start searching for devices. You can do this by calling the "scanForPeripherals" method.*/
  
  func startScan() {
    peripherals = []
    print("Now Scanning...")
    self.timer.invalidate()
    let services = [CBUUID(string:"FEAA")]
    centralManager?.scanForPeripherals(withServices: services , options: nil)
    Timer.scheduledTimer(timeInterval: 5, target: self, selector: #selector(self.cancelScan), userInfo: nil, repeats: false)
    
  }
  
  /*We also need to stop scanning at some point so we'll also create a function that calls "stopScan"*/
  @objc func cancelScan() {
    self.centralManager?.stopScan()
    print("Scan Stopped")
    //print(self.peripherals.description)
    print("Number of Peripherals Found: \(ble_devices.count)")
  }
  
  
  //-Terminate all Peripheral Connection
  /*
   Call this when things either go wrong, or you're done with the connection.
   This cancels any subscriptions if there are any, or straight disconnects if not.
   (didUpdateNotificationStateForCharacteristic will cancel the connection if a subscription is involved)
   */
  func disconnectFromDevice () {
    if blePeripheral != nil {
      // We have a connection to the device but we are not subscribed to the Transfer Characteristic for some reason.
      // Therefore, we will just disconnect from the peripheral
      centralManager?.cancelPeripheralConnection(blePeripheral!)
    }
  }
  
  
  func restoreCentralManager() {
    //Restores Central Manager delegate if something went wrong
    centralManager?.delegate = self
  }
  
  /*
   Called when the central manager discovers a peripheral while scanning. Also, once peripheral is connected, cancel scanning.
   */
  func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral,advertisementData: [String : Any], rssi RSSI: NSNumber) {
    let serviceUUID = CBUUID(string: "FEAA")
    let _RSSI: Int = RSSI.intValue
    if let serviceData = advertisementData[CBAdvertisementDataServiceDataKey]
      as? [NSObject : AnyObject]{
    if let beaconServiceData = serviceData[serviceUUID] as? NSData,
      let URL = BeaconInfo.parseURLFromFrame(frameData: beaconServiceData) {
      print("URL: ", URL.absoluteString!)
      print("Power: ",_RSSI)
      let temp_url = URL.absoluteString!;
      if (temp_url.hasPrefix("https://#")){
        var temp = temp_url.components(separatedBy: "#")
        let url = temp[1]
        print (url)
        let device: [String:Any] = ["URL":url] // React native can't handle NSURL object to console
      let power: [String:Any] = ["Power":_RSSI]
      //var data = [String: Any]()
      //data.append(device)
      //data.append(power)
      if(ble_names.contains(url))
        {
          print("existed ble")
        }
        else
        {
          ble_devices.append(device)
          Power.append(power)
          //ble_devices.append(power)
          ble_names.append(url)
          //ble_devices.append(device)
          //ble_devices.append(power)
        }
      }}}
    blePeripheral = peripheral
    //let pname = blePeripheral?.name
    //print(peripheral)
    //print (blePeripheral?.identifier)
    /*if let unwrapped = blePeripheral?.name {
      print("testing this function")
      //print(peripheral)
      print(unwrapped)
      if(unwrapped.hasPrefix("Spot:")){
        //if(unwrapped.hasPrefix("MyESP")){
        var temp = unwrapped.components(separatedBy: ":")
        print(temp[1])
        var lot_name = temp[1].components(separatedBy: ",")
        print(lot_name[0])
        let device: [String:String] = ["device":temp[1]]
        if(ble_names.contains(unwrapped))
        {
          print("existed ble")
        }
        else
        {
          ble_devices.append(device)
          ble_names.append(unwrapped)
        }
        ble_dev["names"]=unwrapped;
      }
      self.peripherals.append(peripheral)
      self.RSSIs.append(RSSI)
      print(RSSI)
      peripheral.delegate = self
      //self.baseTableView.reloadData()
      //print(peripheral)
      //    }
    }
    */
    if blePeripheral == nil {
      print("Found new pheripheral devices with services")
      print("Peripheral name: \(String(describing: peripheral.name))")
      print("**********************************")
      print ("Advertisement Data : \(advertisementData)")
    }
  }
  
  //Doesn't really need to establish a connection with the BLE
  
  //Peripheral Connections: Connecting, Connected, Disconnected
  
  //-Connection
  /*func connectToDevice () {
    centralManager?.connect(blePeripheral!, options: nil)
  }*/
  
  /*
   Invoked when a connection is successfully created with a peripheral.
   This method is invoked when a call to connect(_:options:) is successful. You typically implement this method to set the peripheral’s delegate and to discover its services.
   */
  //-Connected
  func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
    print("*****************************")
    print("Connection complete")
    print("Peripheral info: \(String(describing: blePeripheral))")
    
    //Stop Scan- We don't need to scan once we've connected to a peripheral. We got what we came for.
    centralManager?.stopScan()
    print("Scan Stopped")
    print(self.peripherals.description)
    //Erase data that we might have
    data.length = 0
    
    //Discovery callback
    peripheral.delegate = self
    
  }
  
  /*
   Invoked when the central manager fails to create a connection with a peripheral.
   */
  
  func centralManager(_ central: CBCentralManager, didFailToConnect peripheral: CBPeripheral, error: Error?) {
    if error != nil {
      print("Failed to connect to peripheral")
      return
    }
  }
  
  func disconnectAllConnection() {
    centralManager.cancelPeripheralConnection(blePeripheral!)
  }
  
  /*
   Invoked when you discover the peripheral’s available services.
   This method is invoked when your app calls the discoverServices(_:) method. If the services of the peripheral are successfully discovered, you can access them through the peripheral’s services property. If successful, the error parameter is nil. If unsuccessful, the error parameter returns the cause of the failure.
   */
  func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
    print("*******************************************************")
    
    if ((error) != nil) {
      print("Error discovering services: \(error!.localizedDescription)")
      return
    }
    
    guard let services = peripheral.services else {
      return
    }
    //We need to discover the all characteristic
    for service in services {
      
      peripheral.discoverCharacteristics(nil, for: service)
      // bleService = service
    }
    print("Discovered Services: \(services)")
  }
  
  /*
   Invoked when you discover the characteristics of a specified service.
   This method is invoked when your app calls the discoverCharacteristics(_:for:) method. If the characteristics of the specified service are successfully discovered, you can access them through the service's characteristics property. If successful, the error parameter is nil. If unsuccessful, the error parameter returns the cause of the failure.
   */
  
  func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
    
    print("*******************************************************")
    
    if ((error) != nil) {
      print("Error discovering services: \(error!.localizedDescription)")
      return
    }
    
    guard let characteristics = service.characteristics else {
      return
    }
    
    print("Found \(characteristics.count) characteristics!")
    
    for characteristic in characteristics {
      //looks for the right characteristic
      
      peripheral.discoverDescriptors(for: characteristic)
    }
  }
  
  // Getting Values From Characteristic
  
  /*After you've found a characteristic of a service that you are interested in, you can read the characteristic's value by calling the peripheral "readValueForCharacteristic" method within the "didDiscoverCharacteristicsFor service" delegate.
   */
  func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
    
    if characteristic == rxCharacteristic {
      if let ASCIIstring = NSString(data: characteristic.value!, encoding: String.Encoding.utf8.rawValue) {
        characteristicASCIIValue = ASCIIstring
        print("Value Recieved: \((characteristicASCIIValue as String))")
        NotificationCenter.default.post(name:NSNotification.Name(rawValue: "Notify"), object: nil)
        
      }
    }
  }
  
  
  func peripheral(_ peripheral: CBPeripheral, didDiscoverDescriptorsFor characteristic: CBCharacteristic, error: Error?) {
    print("*******************************************************")
    
    if error != nil {
      print("\(error.debugDescription)")
      return
    }
    if ((characteristic.descriptors) != nil) {
      
      for x in characteristic.descriptors!{
        let descript = x as CBDescriptor!
        print("function name: DidDiscoverDescriptorForChar \(String(describing: descript?.description))")
        print("Rx Value \(String(describing: rxCharacteristic?.value))")
        print("Tx Value \(String(describing: txCharacteristic?.value))")
      }
    }
  }
  
  
  func peripheral(_ peripheral: CBPeripheral, didUpdateNotificationStateFor characteristic: CBCharacteristic, error: Error?) {
    print("*******************************************************")
    
    if (error != nil) {
      print("Error changing notification state:\(String(describing: error?.localizedDescription))")
      
    } else {
      print("Characteristic's value subscribed")
    }
    
    if (characteristic.isNotifying) {
      print ("Subscribed. Notification has begun for: \(characteristic.uuid)")
    }
  }
  
  
  
  func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
    print("Disconnected")
  }
  
  
  func peripheral(_ peripheral: CBPeripheral, didWriteValueFor characteristic: CBCharacteristic, error: Error?) {
    guard error == nil else {
      print("Error discovering services: error")
      return
    }
    print("Message sent")
  }
  
  func peripheral(_ peripheral: CBPeripheral, didWriteValueFor descriptor: CBDescriptor, error: Error?) {
    guard error == nil else {
      print("Error discovering services: error")
      return
    }
    print("Succeeded!")
  }
  
  /*
   Invoked when the central manager’s state is updated.
   This is where we kick off the scan if Bluetooth is turned on.
   */
  func centralManagerDidUpdateState(_ central: CBCentralManager) {
    if #available(iOS 10.0, *) {
      if central.state == CBManagerState.poweredOn {
        // We will just handle it the easy way here: if Bluetooth is on, proceed...start scan!
        print("Bluetooth Enabled")
        startScan()
        
      } else {
        //If Bluetooth is off, display a UI alert message saying "Bluetooth is not enable" and "Make sure that your bluetooth is turned on"
        print("Bluetooth Disabled- Make sure your Bluetooth is turned on")
        
        let alertVC = UIAlertController(title: "Bluetooth is not enabled", message: "Make sure that your bluetooth is turned on", preferredStyle: UIAlertControllerStyle.alert)
        let action = UIAlertAction(title: "ok", style: UIAlertActionStyle.default, handler: { (action: UIAlertAction) -> Void in
          self.dismiss(animated: true, completion: nil)
        })
        alertVC.addAction(action)
        self.present(alertVC, animated: true, completion: nil)
      }
    } else {
      // Fallback on earlier versions
    }
  }
}
class BeaconID : NSObject {
  
  enum BeaconType {
    case Eddystone              // 10 bytes namespace + 6 bytes instance = 16 byte ID
    case EddystoneEID           // 8 byte ID
  }
  
  let beaconType: BeaconType
  
  ///
  /// The raw beaconID data. This is typically printed out in hex format.
  ///
  let beaconID: [UInt8]
  
  fileprivate init(beaconType: BeaconType!, beaconID: [UInt8]) {
    self.beaconID = beaconID
    self.beaconType = beaconType
  }
  
  override var description: String {
    if self.beaconType == BeaconType.Eddystone || self.beaconType == BeaconType.EddystoneEID {
      let hexid = hexBeaconID(beaconID: self.beaconID)
      return "BeaconID beacon: \(hexid)"
    } else {
      return "BeaconID with invalid type (\(beaconType))"
    }
  }
  
  private func hexBeaconID(beaconID: [UInt8]) -> String {
    var retval = ""
    for byte in beaconID {
      var s = String(byte, radix:16, uppercase: false)
      if s.count == 1 {
        s = "0" + s
      }
      retval += s
    }
    return retval
  }
  
}

func ==(lhs: BeaconID, rhs: BeaconID) -> Bool {
  if lhs == rhs {
    return true;
  } else if lhs.beaconType == rhs.beaconType
    && rhs.beaconID == rhs.beaconID {
    return true;
  }
  
  return false;
}

///
/// BeaconInfo
///
/// Contains information fully describing a beacon, including its beaconID, transmission power,
/// RSSI, and possibly telemetry information.
///
class BeaconInfo : NSObject {
  
  static let EddystoneUIDFrameTypeID: UInt8 = 0x00
  static let EddystoneURLFrameTypeID: UInt8 = 0x10
  static let EddystoneTLMFrameTypeID: UInt8 = 0x20
  static let EddystoneEIDFrameTypeID: UInt8 = 0x30
  
  enum EddystoneFrameType {
    case UnknownFrameType
    case UIDFrameType
    case URLFrameType
    case TelemetryFrameType
    case EIDFrameType
    
    var description: String {
      switch self {
      case .UnknownFrameType:
        return "Unknown Frame Type"
      case .UIDFrameType:
        return "UID Frame"
      case .URLFrameType:
        return "URL Frame"
      case .TelemetryFrameType:
        return "TLM Frame"
      case .EIDFrameType:
        return "EID Frame"
      }
    }
  }
  
  let beaconID: BeaconID
  let txPower: Int
  let RSSI: Int
  let telemetry: NSData?
  
  private init(beaconID: BeaconID, txPower: Int, RSSI: Int, telemetry: NSData?) {
    self.beaconID = beaconID
    self.txPower = txPower
    self.RSSI = RSSI
    self.telemetry = telemetry
  }
  
  class func frameTypeForFrame(advertisementFrameList: [NSObject : AnyObject]) -> EddystoneFrameType {
    let uuid = CBUUID(string: "FEAA")
    if let frameData = advertisementFrameList[uuid] as? NSData {
      if frameData.length > 1 {
        let count = frameData.length
        var frameBytes = [UInt8](repeating: 0, count: count)
        frameData.getBytes(&frameBytes, length: count)
        
        if frameBytes[0] == EddystoneUIDFrameTypeID {
          return EddystoneFrameType.UIDFrameType
        } else if frameBytes[0] == EddystoneTLMFrameTypeID {
          return EddystoneFrameType.TelemetryFrameType
        } else if frameBytes[0] == EddystoneEIDFrameTypeID {
          return EddystoneFrameType.EIDFrameType
        } else if frameBytes[0] == EddystoneURLFrameTypeID {
          return EddystoneFrameType.URLFrameType
        }
      }
    }
    
    return EddystoneFrameType.UnknownFrameType
  }
  
  class func telemetryDataForFrame(advertisementFrameList: [NSObject : AnyObject]!) -> NSData? {
    return advertisementFrameList[CBUUID(string: "FEAA")] as? NSData
  }
  
  ///
  /// Unfortunately, this can't be a failable convenience initialiser just yet because of a "bug"
  /// in the Swift compiler — it can't tear-down partially initialised objects, so we'll have to
  /// wait until this gets fixed. For now, class method will do.
  ///
  class func beaconInfoForUIDFrameData(frameData: NSData, telemetry: NSData?, RSSI: Int) -> BeaconInfo? {
    if frameData.length > 1 {
      let count = frameData.length
      var frameBytes = [UInt8](repeating: 0, count: count)
      frameData.getBytes(&frameBytes, length: count)
      
      if frameBytes[0] != EddystoneUIDFrameTypeID {
        NSLog("Unexpected non UID Frame passed to BeaconInfoForUIDFrameData.")
        return nil
      } else if frameBytes.count < 18 {
        NSLog("Frame Data for UID Frame unexpectedly truncated in BeaconInfoForUIDFrameData.")
      }
      
      let txPower = Int(Int8(bitPattern:frameBytes[1]))
      let beaconID: [UInt8] = Array(frameBytes[2..<18])
      let bid = BeaconID(beaconType: BeaconID.BeaconType.Eddystone, beaconID: beaconID)
      return BeaconInfo(beaconID: bid, txPower: txPower, RSSI: RSSI, telemetry: telemetry)
    }
    
    return nil
  }
  
  class func beaconInfoForEIDFrameData(frameData: NSData, telemetry: NSData?, RSSI: Int) -> BeaconInfo? {
    if frameData.length > 1 {
      let count = frameData.length
      var frameBytes = [UInt8](repeating: 0, count: count)
      frameData.getBytes(&frameBytes, length: count)
      
      if frameBytes[0] != EddystoneEIDFrameTypeID {
        NSLog("Unexpected non EID Frame passed to BeaconInfoForEIDFrameData.")
        return nil
      } else if frameBytes.count < 10 {
        NSLog("Frame Data for EID Frame unexpectedly truncated in BeaconInfoForEIDFrameData.")
      }
      
      let txPower = Int(Int8(bitPattern:frameBytes[1]))
      let beaconID: [UInt8] = Array(frameBytes[2..<10])
      let bid = BeaconID(beaconType: BeaconID.BeaconType.EddystoneEID, beaconID: beaconID)
      return BeaconInfo(beaconID: bid, txPower: txPower, RSSI: RSSI, telemetry: telemetry)
    }
    
    return nil
  }
  
  class func parseURLFromFrame(frameData: NSData) -> NSURL? {
    if frameData.length > 0 {
      let count = frameData.length
      var frameBytes = [UInt8](repeating: 0, count: count)
      frameData.getBytes(&frameBytes, length: count)
      
      if let URLPrefix = URLPrefixFromByte(schemeID: frameBytes[2]) {
        var output = URLPrefix
        for i in 3..<frameBytes.count {
          if let encoded = encodedStringFromByte(charVal: frameBytes[i]) {
            output.append(encoded)
          }
        }
        
        return NSURL(string: output)
      }
    }
    
    return nil
  }
  
  override var description: String {
    switch self.beaconID.beaconType {
    case .Eddystone:
      return "Eddystone \(self.beaconID), txPower: \(self.txPower), RSSI: \(self.RSSI)"
    case .EddystoneEID:
      return "Eddystone EID \(self.beaconID), txPower: \(self.txPower), RSSI: \(self.RSSI)"
    }
  }
  
  class func URLPrefixFromByte(schemeID: UInt8) -> String? {
    switch schemeID {
    case 0x00:
      return "http://www."
    case 0x01:
      return "https://www."
    case 0x02:
      return "http://"
    case 0x03:
      return "https://"
    default:
      return nil
    }
  }
  
  class func encodedStringFromByte(charVal: UInt8) -> String? {
    switch charVal {
    case 0x00:
      return ".com/"
    case 0x01:
      return ".org/"
    case 0x02:
      return ".edu/"
    case 0x03:
      return ".net/"
    case 0x04:
      return ".info/"
    case 0x05:
      return ".biz/"
    case 0x06:
      return ".gov/"
    case 0x07:
      return ".com"
    case 0x08:
      return ".org"
    case 0x09:
      return ".edu"
    case 0x0a:
      return ".net"
    case 0x0b:
      return ".info"
    case 0x0c:
      return ".biz"
    case 0x0d:
      return ".gov"
    default:
      return String(data: Data(bytes: [ charVal ] as [UInt8], count: 1), encoding: .utf8)
    }
  }
  
}

