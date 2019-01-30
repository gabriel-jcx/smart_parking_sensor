import { StyleSheet, Text, View, Image, TouchableWithoutFeedback, StatusBar, TextInput, SafeAreaView, 
         Keyboard, TouchableOpacity, KeyboardAvoidingView } from 'react-native';
import React from 'react';
import {StackNavigator} from 'react-navigation';

export default class Splash extends React.Component {
  
  //Splash Screen Timeout Settings
  componentWillMount() 
  {
    setTimeout(()=>{
      this.props.navigation.navigate('Intro');
    }, 1000)
  }

  render() {
    const {navigate} = this.props.navigation;
    return (
        <View style={styles.container}>
          <Image source={require ('../../images/slug.jpg')} />
        </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    transform: [{ scale: 0.50 }],
    flex: 1,
    backgroundColor: 'rgb(0,70,122)',
    alignItems: 'center',
    justifyContent: 'center',
  },

  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    marginBottom: 200
  },

  logo: {
    width: 128,
    height: 56,
    marginBottom: 40
  }

});
