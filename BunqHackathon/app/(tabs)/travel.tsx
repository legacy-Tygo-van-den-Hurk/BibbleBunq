// File: app/(tabs)/travel.tsx
import { MaterialCommunityIcons } from '@expo/vector-icons';
import axios from 'axios';
import { useCallback } from 'react';
import { Alert, Image, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useRouter } from 'expo-router';




export default function TravelScreen() {
  const router = useRouter();

  const handleSafetyPress = useCallback(async () => {
    try {
      const cityRes = await fetch('https://ipinfo.io/city');
      const city = (await cityRes.text()).trim();

      const response = await axios.post('http://192.168.248.170:5000/process_city', {
        city,
      });

      router.push({
        pathname: '/safety',
        params: { data: JSON.stringify(response.data) },
      });
    } catch (err) {
      console.error(err);
      Alert.alert('Error', 'Could not complete the safety check.');
    }
  }, []);
  
  return (
    <ScrollView style={{ flex: 1, backgroundColor: '#000' }}>
      <Text style={styles.header}>Travel</Text>

      <Text style={styles.subHeader}>What's Happening</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.cardRow}>
        {[1, 2].map((_, i) => (
          <View key={i} style={styles.card}>
            <Image
              source={require('../../assets/images/house.jpg')}
              style={styles.cardImage}
            />
            <Text style={styles.cardTitle}>Location Name</Text>
            <Text style={styles.cardSubtitle}>🇳🇱 Eindhoven</Text>
            <Text style={styles.cardSubtitle}>Recommended by Ege 4 days ago</Text>
          </View>
        ))}
      </ScrollView>

      <View style={styles.stretchedRow}>
        <TouchableOpacity style={[styles.equalButton, { backgroundColor: '#002b5c' }]}>
          <MaterialCommunityIcons name="silverware-fork-knife" size={26} color="#4da6ff" />
          <Text style={[styles.columnText, { color: '#4da6ff' }]}>Eat</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.equalButton, { backgroundColor: '#004225' }]}>
          <MaterialCommunityIcons name="glass-cocktail" size={26} color="#66ffcc" />
          <Text style={[styles.columnText, { color: '#66ffcc' }]}>Drink</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.equalButton, { backgroundColor: '#4b0000' }]}>
          <MaterialCommunityIcons name="basketball" size={26} color="#ff6666" />
          <Text style={[styles.columnText, { color: '#ff6666' }]}>Fun</Text>
        </TouchableOpacity>
      </View>






      <View style={styles.finnCard}>
        <Text style={styles.finnTitle}>Find Places You’ll Love</Text>
        <Text style={styles.finnSubtitle}>Use the power of Finn to get place recommendations, tailored to your lifestyle!</Text>
        <TouchableOpacity><Text style={styles.finnLink}>Find Places with Finn</Text></TouchableOpacity>
      </View>

      <Text style={styles.subHeader}>For Your Trip</Text>
      <View style={styles.cardRow}>
        <View style={[styles.featureCard, { marginRight: 8 }]}>
          <MaterialCommunityIcons name="shield-check" size={36} color="#4da6ff" />
          <Text style={styles.featureTitle}>Travel Insurance</Text>
          <Text style={styles.featureSubtitle}>Inactive</Text>
        </View>

        <View style={[styles.featureCard, { marginLeft: 8 }]}>
          <MaterialCommunityIcons name="sim" size={36} color="#66ffcc" />
          <Text style={styles.featureTitle}>Get an eSIM</Text>
          <Text style={styles.featureSubtitle}>Save up to 90%{'\n'}on roaming</Text>
        </View>
      </View>



      <View style={styles.countryContainer}>
      <TouchableOpacity style={styles.countrySelector}>
  <Text style={styles.countrySelectorText}>🇳🇱 Netherlands</Text>
  <MaterialCommunityIcons name="chevron-down" size={16} color="#fff" />
</TouchableOpacity>


  {/* Tip Items */}
  {[
    {
      icon: 'pause-circle',
      color: '#cc3300',
      title: 'Your cards are not enabled here',
      subtitle: 'Tap here to enable your card(s) for Netherlands',
    },
    {
      icon: 'wallet',
      color: '#ff6600',
      title: 'Bring a debit card',
      subtitle:
        'Your bunq card works nearly everywhere here, but some places only accept Debit Cards. If you want some cash as a backup, most people withdraw around €60.',
    },
    {
      icon: 'percent',
      color: '#ff0066',
      title: 'Tipping is appreciated',
      subtitle:
        'You’re not required to tip here, but it is appreciated. If you want to tip, the standard would be to round up the bill.',
    },
    {
      icon: 'power-plug',
      color: '#ffcc00',
      title: 'European plugs work here',
      subtitle: 'No need to bring an adapter!',
    },
    {
      icon: 'shield-alert',
      color: '#3399ff',
      title: 'Learn about the safety conditions around your area',
      subtitle: 'Let Bibble assess how secure your area is',
    },
  ].map((item, i) => (
    <TouchableOpacity
      key={i}
      style={[
        styles.tipItem,
        styles.tipRow,
        item.title === 'Learn about the safety conditions around your area' && styles.tipHighlightRow,
      ]}
      onPress={
        item.title === 'Learn about the safety conditions around your area'
          ? handleSafetyPress
          : undefined
      }
      activeOpacity={0.7}
    >

      <View style={[styles.tipIconCircle, { backgroundColor: item.color }]}>
        <MaterialCommunityIcons name={item.icon} size={20} color="#fff" />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={styles.tipTitle}>{item.title}</Text>
        <Text style={styles.tipSubtitle}>{item.subtitle}</Text>
      </View>
    </TouchableOpacity>
  ))}
</View>

<Text style={styles.subHeader}>Travel Stats</Text>

<View style={styles.statsContainer}>
  <Image
    source={require('../../assets/images/map-dark.jpg')} // Add a suitable dark map image
    style={styles.mapImage}
    resizeMode="cover"
  />

  <View style={styles.statCardRow}>
    <View style={styles.statCard}>
      <Text style={styles.statTitle}>0</Text>
      <Text style={styles.statSubtitle}>Countries Visited</Text>
    </View>
    <View style={styles.statCard}>
      <Text style={styles.statTitle}>€0,00</Text>
      <Text style={styles.statSubtitle}>Saved With ZeroFX</Text>
    </View>
  </View>
</View>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  header: { color: '#fff', fontSize: 28, fontWeight: 'bold', margin: 16 },
  subHeader: { color: '#fff', fontSize: 20, fontWeight: '600', marginLeft: 16, marginTop: 20 },
  cardRow: { flexDirection: 'row', paddingLeft: 16 },
  card: { backgroundColor: '#222', borderRadius: 12, marginRight: 12, padding: 10, width: 180 },
  cardImage: { width: '100%', height: 100, borderRadius: 8 },
  cardTitle: { color: '#fff', fontWeight: 'bold', marginTop: 8 },
  cardSubtitle: { color: '#ccc', fontSize: 12 },

  buttonRow: { flexDirection: 'row', justifyContent: 'space-around', marginTop: 20 },
  button: { backgroundColor: '#333', padding: 12, borderRadius: 8 },
  buttonText: { color: '#fff' },

  finnCard: { backgroundColor: '#1a1a1a', padding: 16, margin: 16, borderRadius: 10 },
  finnTitle: { color: '#fff', fontSize: 16, fontWeight: '600' },
  finnSubtitle: { color: '#ccc', marginVertical: 6 },
  finnLink: { color: 'deepskyblue' },

  tripRow: { flexDirection: 'row', justifyContent: 'space-around', marginVertical: 10 },
  tripItem: { backgroundColor: '#222', padding: 16, borderRadius: 10 },
  tripText: { color: '#fff' },

  tipItem: { padding: 16, borderBottomColor: '#333', borderBottomWidth: 1 },

  statsRow: { flexDirection: 'row', justifyContent: 'space-around', marginVertical: 20 },

  stretchedRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 16,
    paddingHorizontal: 16,
  },
  equalButton: {
    width: '30%',
    aspectRatio: 1.3, // keeps width-to-height ratio consistent
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 12,
  },
  columnText: {
    fontSize: 14,
    fontWeight: '600',
    marginTop: 6,
  },
  
  featureCard: {
    backgroundColor: '#1c1c1e',
    borderRadius: 16,
    padding: 16,
    width: '45%',
    alignItems: 'center',
  },
  featureTitle: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
    marginTop: 8,
  },
  featureSubtitle: {
    color: '#aaa',
    fontSize: 12,
    textAlign: 'center',
    marginTop: 4,
  },
  countryContainer: {
    backgroundColor: '#1a1a1a',
    borderRadius: 16,
    padding: 16,
    marginHorizontal: 16,
    marginTop: 20,
  },
  countryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  countryFlag: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  
  tipRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  tipIconCircle: {
    width: 32,
    height: 32,
    borderRadius: 16,
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  tipTitle: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
    marginBottom: 2,
  },
  tipSubtitle: {
    color: '#ccc',
    fontSize: 12,
  },
  countrySelector: {
    flexDirection: 'row',
    alignSelf: 'flex-start',
    backgroundColor: '#2a2a2c',
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
    alignItems: 'center',
    marginBottom: 16,
  },
  countrySelectorText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
    marginRight: 4,
  },
  tipHighlightRow: {
    backgroundColor: '#0a1a2f',
    borderRadius: 12,
    padding: 12,
    borderBottomWidth: 0, // override bottom border
  },
  
  statsContainer: {
    marginTop: 20,
    marginHorizontal: 16,
  },
  mapImage: {
    width: '100%',
    height: 150,
    borderRadius: 12,
    marginBottom: 12,
  },
  statCardRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statCard: {
    backgroundColor: '#1c1c1e',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 12,
    flex: 1,
    alignItems: 'center',
    marginHorizontal: 4,
  },
  statTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  statSubtitle: {
    color: '#aaa',
    fontSize: 12,
    textAlign: 'center',
    marginTop: 4,
  },
  
  
});
