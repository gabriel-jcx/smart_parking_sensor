/*
   This is a depricated page!!! DO NOT USE!
*/



import React from 'react';
import { StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import LoginForm from './LoginForm';

export default class Login extends React.Component {
  render() {
    return (
        <View style={styles.formContainer}>
        <LoginForm />
        </View>
    );
  }
}

const styles = StyleSheet.create({
  
  container: {
    flex: 1,
    backgroundColor: 'rgb(0,70,122)',
    flexDirection: 'column'
  },

});
