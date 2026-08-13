import React from 'react';
import { SafeAreaView, StyleSheet, StatusBar } from 'react-native';
import { AppNavigator } from './src/navigation';

export default function App() {
  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0F172A" />
      <AppNavigator />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
});
