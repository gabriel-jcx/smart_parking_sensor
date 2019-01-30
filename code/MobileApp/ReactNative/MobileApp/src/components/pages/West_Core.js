import React from 'react';
import { StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import {StackNavigator} from 'react-navigation';
import { Button } from 'react-native';

export default class West_Core extends React.Component {
  render() {
    var {navigate} = this.props.navigation;
    return (
      <View style={styles.container}>
      <Text style={styles.title}> West Core </Text> 
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