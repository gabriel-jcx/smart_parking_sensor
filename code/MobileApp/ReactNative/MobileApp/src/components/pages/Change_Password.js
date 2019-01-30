import React from 'react';
import { AsyncStorage,StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
//import googlecloud;
import {StackNavigator} from 'react-navigation';
export default class Change_Password extends React.Component {
   constructor(props){
      super(props);
      this.state = {
          navigation: this.props.navigation,
          username:'123',
          oldpasswd:'',
          newpasswd:'',
      }
   }
   async getKey(){
      try{
         return await AsyncStorage.getItem('userId')
      } catch(error){
         console.log("Error retrieveing");
      }
   }
   async componentWillMount(){
      const {navigate} = this.props.navigation;
      const userId = await this.getKey();
      console.log(userId);
      if (userId !== null)
      {
         this.state.username = userId;
         console.log(this.state.username);
         console.log("username variable setted");
      }else{
         alert("You need to login first");
         navigate("Parking_Spots");
      }
   }
  render() {
    return (
      <View style={styles.container}>
        
        <View style={styles.logoContainer}> 
        <Image source={require ('../../images/UCSC_Logo.jpg')} />
        </View>

        <TextInput 
        placeholder="Old Password"
        placeholderTextColor="grey"
        style = {styles.input}
        onChangeText={(oldpasswd) => this.setState({oldpasswd})}
        />

        <TextInput 
        placeholder="New Password"
        placeholderTextColor="grey"
        style = {styles.secondinput}
        onChangeText={(newpasswd) => this.setState({newpasswd})}
        />

        <TouchableOpacity style={styles.buttonContainer}
          onPress={this.change_pass}>
          <Text style={styles.buttonText}> Change </Text>
        </TouchableOpacity>
      
      </View>
    );
  }
  change_pass = () => {
     var {navigate} = this.state.navigation;
     console.log(this.state.username);
     console.log("i got here");
     console.log(this.state.username);
     fetch('https://structure1-0.appspot.com/authenticate/changepasswd',{
     //fetch('http://127.0.0.1:8080/authenticate/changepasswd',{
        method: 'POST',
        hearders:{
           Accept: 'application/json',
           'Content-Type': 'application/json',
        },
        body: JSON.stringify({
           'username':this.state.username,
           'oldpassword':this.state.oldpasswd,
           'newpassword':this.state.newpasswd
        })
     }).then((response)=>response.json())//=>console.log(response));
     .then((responseJson) =>{
        console.log(responseJson);
        console.log(responseJson.stat);
        alert(responseJson.stat);
        if(responseJson.stat == "Success"){
           console.log("Change Success");
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
