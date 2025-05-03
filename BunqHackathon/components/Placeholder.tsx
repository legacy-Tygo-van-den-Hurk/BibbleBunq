import { View, Text } from 'react-native';

export default function Placeholder({ name }: { name: string }) {
  return (
    <View style={{ flex: 1, backgroundColor: '#000', alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ color: '#fff', fontSize: 24 }}>{name} Page</Text>
    </View>
  );
}
