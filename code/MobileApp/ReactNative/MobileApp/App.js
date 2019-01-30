import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {StackNavigator} from 'react-navigation';
import {RSA} from 'react-native-rsa-native';
import Splash from './src/components/pages/Splash.js';
import Intro from './src/components/pages/Intro.js';
import Login from './src/components/pages/Login.js';
import LoginForm from './src/components/pages/LoginForm.js';
import Parking_Spots from './src/components/pages/Parking_Spots.js';
import West_Remote from './src/components/pages/West_Remote.js';
import West_Core from './src/components/pages/West_Core.js';
import East_Remote from './src/components/pages/East_Remote.js';
import North_Remote from './src/components/pages/North_Remote.js';
import Beacon from './src/components/pages/Beacon.js';
import Change_Password from './src/components/pages/Change_Password.js';
import { NativeModules } from 'react-native';

const Navigation = StackNavigator({
  // A test on the timer of reactnative to add some animation feature lol
  Splash: {
     screen: Splash,
     navigationOptions:{
        header:null,
        headerLeft:null,
     },
  },
  // The main menu module 
  Intro: { 
     screen: Intro,
     navigationOptions:{
        header:null,
        headerLeft:null,
     },
  },
  // Login page for the user
  LoginForm: {
     screen: LoginForm,
     navigationOptions:{
     }
  },
  // Prototype for BLE, Depricated
  Beacon: {
     screen: Beacon,
     navigationOptions:{
     },
  },
  // A lot menu
  Parking_Spots: {
     screen: Parking_Spots,
     navigationOptions:{
     },
  },
  North_Remote: {
     screen: North_Remote,
     navigationOptions:{
     },
  },
  East_Remote: {
     screen: East_Remote,
     navigationOptions:{
     },
  },
  West_Core: {
     screen: West_Core,
     navigationOptions:{
     },
  },
  West_Remote: {
     screen: West_Remote,
     navigationOptions:{
     },
  },
  // module for user to change password
  Change_Password: {
     screen: Change_Password,
     navigationOption:{
     },
  },
  });
export default Navigation;
