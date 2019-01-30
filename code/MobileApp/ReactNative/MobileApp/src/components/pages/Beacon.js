import { AsyncStorage, StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import React from 'react';
import {StackNavigator} from 'react-navigation';
import { Button } from 'react-native';
import BleManager from 'react-native-ble-manager';
//import Beacons from 'react-native-beacons-manager';
import { NativeModules } from 'react-native';



export default class Beacon extends React.Component {
  constructor (props){
     super(props);
     this.state = {
        bloom:[],
        iv:[]
     }
     //this.state= 'sdfasd';
  }
  async start_ble(){
    // console.log(NativeModule);
     NativeModules.ViewController.BloomEncrypt("test",(err,bloom,iv)=>{
        console.log(bloom);
        console.log(iv);
        this.state.bloom = bloom;
        this.state.iv = iv;
        //console.log(r);
        console.log("callback done");
        //console.log("The state bloom is")
        //console.log(this.state.bloom);
        //console.log("The stae iv is")
        //console.log(this.state.iv);
        fetch('https://structure1-0.appspot.com/bloom_filter',{
        //fetch('http://127.0.0.1:8080/usr/map_ble',{
           method: 'POST',
           headers:{
              Accept: 'application/json',
              'Content-Type': 'application/json',
           },
           body: JSON.stringify({
              'bloom':this.state.bloom,
              'iv': this.state.iv
           })
        }).then((response)=>console.log(response))
     });
  }
  new_func = () => {
     console.log("Native Modules Viewcontroller finished its job!");
  }
  render() {
    const {navigate} = this.props.navigation;
    return (
      <View style={styles.container}>
      <TouchableOpacity
        style={styles.button}
        onPress={()=>this.start_ble()}
        >
        <Text style={styles.buttontext}> Bloom Encrypt </Text>
      </TouchableOpacity>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'rgb(0,70,122)',
    alignItems: 'center',
    justifyContent: 'center',
  },

  title: {
    height: 60,
    fontWeight: 'bold',
    fontSize: 40,
    color: 'white',
    marginBottom: 270
  },

  buttontext: {
    fontWeight: 'bold',
    fontSize: 20,
    textAlign: 'center',
    color: 'yellow'
  },
    
  button: {
    backgroundColor: '#2980b9',
    width: 300,
    borderRadius: 25,
    marginVertical: 10,
    paddingVertical: 13,
    marginBottom: 20
  }

});
