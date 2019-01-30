import React from 'react';
import { AsyncStorage,StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
//import googlecloud;
import {StackNavigator} from 'react-navigation';
import {RSA,RSAKeychain} from 'react-native-rsa-native';


export default class LoginForm extends React.Component {
   // The key states initialized in the constructor
   constructor(props){
      super(props);
      this.state = {
          navigation: this.props.navigation,
          username:'',
          passwd:'',
      }
   }
  // The render function, however instead of using setState for username and
  // password, its better to use a single variable, this is due to earlier
  // ignorance of me on react native;)
  render() {
    return (
      <View style={styles.container}>
        
        <View style={styles.logoContainer}> 
        <Image source={require ('../../images/UCSC_Logo.jpg')} />
        </View>

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
  // Function to save the userId value into asyncStorage for persistent login
  async saveKey(value){
     try{
       await AsyncStorage.setItem('userId',value);
     } catch (error){
        console.log("Error saving data");
     }

  }
  // This function used to verify the value of saved userId
  async getKey(){
     try{
        const value = await AsyncStorage.getItem('userId');
        console.log(value);
     } catch(error){
        console.log("Error retrieveing");
     }
  }
  // Function would get executed when button onclick
  auth_user = () => {
     console.log(RSA);
     var {navigate} = this.state.navigation;
     console.log("i got here");
     // Send a POST request to the web app
     fetch('https://structure1-0.appspot.com/authenticate/usr',{
     //fetch('http://127.0.0.1:8080/authenticate/usr',{
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
           this.saveKey(responseJson.studentID);
           this.getKey();
           navigate("Parking_Spots");
        }
     })
     .catch((error) =>{
        console.error(error);
     });
  }
}

//Style Sheet
const styles = StyleSheet.create({
  
container: {
    padding: 20,
    flex: 1,
    backgroundColor: 'rgb(0,70,122)',
    flexDirection: 'column'
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
  },

  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1
  },

  logo: {
    width: 128,
    height: 56,
    marginBottom: 40
  }

});
