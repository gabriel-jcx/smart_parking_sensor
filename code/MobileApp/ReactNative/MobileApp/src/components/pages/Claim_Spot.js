/*
   Another DEPRICATED page
*/

import React from 'react';
import { AsyncStorage,StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import {StackNavigator} from 'react-navigation';
export default class LoginForm extends React.Component {
   constructor(props){
      super(props);
      this.state = {
          navigation: this.props.navigation,
          username:'',
          passwd:'',
      }
   }
  render() {
    return (
      <View style={styles.container}>
        <TextInput 
        placeholder="Student ID"
        placeholderTextColor="grey"
        style = {styles.input}
        onChangeText={(username) => this.setState({username})}
        />
        <TextInput 
        placeholder="Blue Password"
        placeholderTextColor="grey"
        style = {styles.secondinput}
        onChangeText={(passwd) => this.setState({passwd})}
        />
        <TouchableOpacity style={styles.buttonContainer}
          onPress={this.auth_user}>
          <Text style={styles.buttonText}> LOGIN </Text>
        </TouchableOpacity>
      </View>
    );
  }
  async wait_auth(){
     var ID = await AsyncStorage.getItem(studentID);
  }
  auth_user = () => {
     var {navigate} = this.state.navigation;
     console.log("i got here");
//     fetch('http://structure1-0.appspot.com/authenticate/usr',{
     fetch('http://127.0.0.1:8080/authenticate/usr',{
        method: 'POST',
        hearders:{
           Accept: 'application/json',
           'Content-Type': 'application/json',
        },
        body: JSON.stringify({
           'username':this.state.username,
           'password':this.state.passwd
        })
     }).then((response)=>response.json())//=>console.log(response));
     .then((responseJson) =>{
        console.log(responseJson);
        console.log(responseJson.studentID);
        if(responseJson.studentID == "Invalid"){
           alert("Invalid Login");
        }
        else{
           console.log("Login successfull");
           AsyncStorage.multiSet([
              ['userId',responseJson.studentID]
           ]);
           navigate("Parking_Spots");
        }
        //AsyncStorage.multiSet(responseJson); 
     })
     .catch((error) =>{
        console.error(error);
     });
     //const mobile_user = datastore.get(new_key); 
      
     //alert(mobile_user);
  }
}

const styles = StyleSheet.create({
  
  container: {
    padding: 20
  },
  
  input: {
    height: 40,
    backgroundColor: 'white',
    marginBottom: 40,
    color: 'blue',
    paddingHorizontal: 10
  },

    secondinput: {
    height: 40,
    backgroundColor: 'white',
    marginBottom: 300,
    color: 'blue',
    paddingHorizontal: 10
  },

  buttonContainer:{
    backgroundColor: '#2980b9',
    width: 345,
    borderRadius: 25,
    marginVertical: 10,
    paddingVertical: 13
  },

  buttonText:{
    fontWeight: 'bold',
    fontSize: 20,
    textAlign: 'center',
    color: 'yellow'
  }

});
