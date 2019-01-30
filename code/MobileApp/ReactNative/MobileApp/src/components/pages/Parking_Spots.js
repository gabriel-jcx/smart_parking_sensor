import React from 'react';
import { AsyncStorage, StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import {StackNavigator} from 'react-navigation';
import { Button } from 'react-native';
import { NativeModules } from 'react-native';

export default class Parking_Spots extends React.Component {
  constructor(props){
     super(props);
     this.state ={
        bloom:'',
        iv: '',
        westRemote:'',
        eastRemote:'',
        northRemote:'',
     };
  }
  async removeKey(){
     try{
        await AsyncStorage.removeItem('userId');
     } catch (error){
        console.log("error resetting");
        console.log(error);
     }
  }
  componentWillMount(){
     NativeModules.ViewController.BloomEncrypt("test",(err,bloom,iv)=>{
        console.log(bloom);
        console.log(iv);
        this.state.bloom = bloom;
        this.state.iv = iv;
        //console.log(r);
        console.log("callback done");
        fetch('https://structure1-0.appspot.com/usr/query_stats',{
           method: 'POST',
           headers:{
              Accept: 'application/json',
              'Content-Type': 'application/json',
           },
           body: JSON.stringify({
              'iv':iv,
              'bloom':bloom,
           })
        }).then((response)=>response.json())
        .then((responseJson) =>{
           console.log(responseJson);
           console.log(responseJson.west_percentage);
           console.log(responseJson.east_percentage);
           console.log(responseJson.north_percentage);
           this.setState({westRemote : responseJson.west_percentage}); 
           this.setState({eastRemote : responseJson.east_percentage});
           this.setState({northRemote: responseJson.north_percentage});
        })
     });
  }
  render() {
    var {navigate} = this.props.navigation;
    return (
      <View style={styles.container}>
      <Text style={styles.title}> Parking Lots </Text>
      <Text style ={styles.subtitle}> Please choose a parking lot </Text>
      <Button onPress={()=>navigate("Change_Password")}
      title="Change Password"
      />

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("North_Remote")}
      >
      <Text style={styles.buttontext}> North Remote {this.state.northRemote}%</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("East_Remote")}
      >
      <Text style={styles.buttontext}> East Remote {this.state.eastRemote}% </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("West_Remote")}
      >
      <Text style={styles.buttontext}> West Remote {this.state.westRemote}%</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("West_Core")}
      >
      <Text style={styles.buttontext}> West Core </Text>
      </TouchableOpacity>
      <Button onPress={()=>this.log_out()}
      title="Log Out"
      />
      </View>
    );
  }
  log_out(){
     this.removeKey();
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
    marginTop: 10,
    fontWeight: 'bold',
    fontSize: 40,
    color: 'white',
    marginBottom: 30
  },

  subtitle: {
    height: 30,
    fontWeight: 'bold',
    fontSize: 18,
    color: 'white',
    marginBottom: 50
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
