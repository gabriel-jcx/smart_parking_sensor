import React from 'react';
import { AsyncStorage, Picker,StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView ,ScrollView} from 'react-native';
import {StackNavigator} from 'react-navigation';
import { Button } from 'react-native';
import { NativeModules } from 'react-native';

export default class West_Remote extends React.Component {
   constructor(props){
     super(props);
     this.state ={
        spot: '',
        studentId: '',
        data: [
         ],
        //ble:[],
     };
  }
  // Get the userId from storage
  async getKey(){
     try{
        return await AsyncStorage.getItem('userId')
     } catch (error){
        console.log("Error retrieveing")
     }
  }
  // After the component of the page mounted,
  // the fucntion starts the Swift native BLE module that return the array
  // of BLE devices
  async componentDidMount(){
     // React native Native Module allows the bridging between
     // the native swift code and the react native
     NativeModules.ViewController.StartBLE((err,r,p)=>{
        var count = 0;
        var wrong_lot = 0;
        console.log(r,p);
        for (count in r) {
           console.log(r[count].URL);
           console.log(p[count].Power);
           // The following if statement need to be adjust in the future
           // since the BLE device are currently named by WestRemote
           /*if(r[count].device[0] == "W"){
              console.log("In the west remote");
              r[count].device = r[count].device.slice(3);
              console.log(r[count].device);
           }else{
              console.log("Wrong lot");
              console.log(r[count]);
              r.splice(count,1);
              console.log(r[count]);
              wrong_lot = 1;
           }*/
        }
        console.log(r.length);
        fetch('https://structure1-0.appspot.com/usr/map_ble',{
        //fetch('http://127.0.0.1:8080/usr/map_ble',{
           method: 'POST',
           headers:{
              Accept: 'application/json',
              'Content-Type': 'application/json',
           },
           body: JSON.stringify(r)
        }).then((response)=>response.json())
        .then((responseJson)=>{
           console.log("The corresponding spot id is: ")
           console.log(responseJson);
           for (i in responseJson.spots){
              console.log(responseJson.spots[i]);
              if(responseJson.spots[i].startsWith("East-Remote")){
              console.log("stared with west remote");
              responseJson.spots[i] = responseJson.spots[i].slice(12);
              }else{
                console.log("not started with east remote");
                responseJson.spots.splice(i,1);
              }
           }
           this.setState({data:responseJson.spots});
        });
        // Need to alert user they are in the wrong lot???
        /*if(wrong_lot){
           alert("You're in the wrong lot");
        }else if(r.length == 0){
           alert("No visible bluetooth devices");
        }else{
           // Set state would force a re-render to display the
           // BLE devices in a scroll list
           this.setState({data:r});
        }*/
     });
     const {navigate} = this.props.navigation;
     const userId = await this.getKey();
     console.log(userId);
     console.log(userId);
     if(userId !== null){
        this.state.studentId = userId;
        console.log("The studentId is now: " + this.state.studentId);
     }else{
        alert("Need to log in first to claim");
        navigate("Intro");
     }
  }
  render() {

    var {navigate} = this.props.navigation;
    return (
      <View style={styles.container}>
      <Text style={styles.title}> West Remote </Text> 
      <View style = {styles.content}>
       <View style = {styles.inputContainer}>
       <Text style={styles.input}> {this.state.spot} </Text>
       </View>
      <Picker
       selectedVlaue = {this.state.spot}
       onValueChange = {itemValue => this.setState({spot:itemValue})}>
       {this.state.data.map((i,index) => (
          <Picker.Item key={index} label={i} value={i}/>
       ))}
      </Picker>
      </View>
      <TouchableOpacity style = {styles.button} onPress={()=> this.claim_spot()}>
       <Text style ={styles.buttontext}>Claim this spot</Text>
      </TouchableOpacity>
      </View>
       
    );
  }
  // Function get executed when claim is pressed
  claim_spot = () =>{
     console.log("the spot id is:"+ this.state.spot);
     fetch('https://structure1-0.appspot.com/authenticate/usr/claim_space',{
     //fetch('http://127.0.0.1:8080/authenticate/usr/claim_space',{
        method: 'POST',
        headers:{
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
           'lot': "East-Remote",
           'spot': this.state.spot,
           'id': this.state.studentId
        })
     }).then((response) => response.json())
     .then((responseJson)=>{
        console.log(responseJson);
        // Tell the user his claim status
        alert(responseJson.status);
     });
  }

}
// Style sheets
const styles = StyleSheet.create({
  input: {
     height: 40,
     backgroundColor: 'white',
     color: 'black',
     paddingHorizontal:110,
  },
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
    marginBottom: 100
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