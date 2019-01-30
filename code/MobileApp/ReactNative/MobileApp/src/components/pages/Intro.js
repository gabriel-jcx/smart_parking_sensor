import { AsyncStorage, StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import React from 'react';
import {StackNavigator} from 'react-navigation';
import { Button } from 'react-native';

export default class Intro extends React.Component {
  //The get key function to retrieve the stored user ID 
  async getKey(){
     try{
        const value = await AsyncStorage.getItem('userId')
        console.log(value);
        return value;
     } catch(error){
        console.log("Error retrieveing");
     }
  }
  async removeKey(){
     try{
        await AsyncStorage.removeItem('userId');
     } catch (error){
        console.log("error resetting");
        console.log(error);
     }
  }
  // Before any component mounts, the function get executed to retrieve the key
  // If the user were logged in, navigate to the parking spots page. 
  async componentWillMount(){
     const {navigate} = this.props.navigation;
     //this.removeKey();
     const userId = await this.getKey();
     console.log(userId);
     if(userId !== null)
     {
        navigate("Parking_Spots");
     }
  }
  //Function acts like html that renders the page
  render() {
    const {navigate} = this.props.navigation;
    return (
      <View style={styles.container}>
      <Text style={styles.title}> UCSC Parking </Text> 

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("LoginForm")}
        >
        <Text style={styles.buttontext}> Student </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("Parking_Spots")}
        >
        <Text style={styles.buttontext}> Guest </Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.button}
        onPress={()=> navigate("Beacon")}
        >
        <Text style={styles.buttontext}> Bloom Test </Text>
      </TouchableOpacity>
      </View>
    );
  }
}
// CSS for the components
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
    marginBottom: 250
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
  },

  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    marginBottom: 170
  },

  logo: {
    width: 128,
    height: 56,
    marginBottom: 40
  }

});
