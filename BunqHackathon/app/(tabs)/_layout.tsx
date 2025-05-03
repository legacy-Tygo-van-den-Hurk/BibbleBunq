import { Tabs } from 'expo-router';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { View, Text } from 'react-native';


export default function TabLayout() {
  return (
    <Tabs
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#1a1a1a',
          borderTopWidth: 0,
        },
        tabBarActiveTintColor: '#1e90ff',
        tabBarInactiveTintColor: '#999',
        tabBarLabelStyle: {
          fontSize: 10,
        },
        tabBarIcon: ({ color, size }) => {
          let iconName: string;

          switch (route.name) {
            case 'index':
              iconName = 'home';
              break;
            case 'travel':
              iconName = 'airplane';
              break;
            case 'budgeting':
              iconName = 'chart-pie';
              break;
            case 'stocks':
              iconName = 'chart-bar';
              break;
            case 'crypto':
              iconName = 'shield';
              break;
            default:
              iconName = 'help-circle-outline';
          }

          return (
            <View style={{ alignItems: 'center' }}>
              <MaterialCommunityIcons name={iconName} size={20} color={color} />
              {route.name === 'crypto' && (
                <View
                  style={{
                    position: 'absolute',
                    top: -6,
                    right: -10,
                    backgroundColor: '#444',
                    paddingHorizontal: 4,
                    borderRadius: 4,
                  }}
                >
                  <Text style={{ fontSize: 8, color: '#aaa', fontWeight: 'bold' }}>BETA</Text>
                </View>
              )}
            </View>
          );
        },
      })}
    >
      <Tabs.Screen name="index" options={{ tabBarLabel: 'Home' }} />
      <Tabs.Screen name="travel" options={{ tabBarLabel: 'Travel' }} />
      <Tabs.Screen name="budgeting" options={{ tabBarLabel: 'Budgeting' }} />
      <Tabs.Screen name="stocks" options={{ tabBarLabel: 'Stocks' }} />
      <Tabs.Screen name="crypto" options={{ tabBarLabel: 'Crypto' }} />
    </Tabs>
  );
}
