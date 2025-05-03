// File: app/safety.tsx
import { useLocalSearchParams } from 'expo-router';
import React from 'react';
import { Dimensions, ScrollView, StyleSheet, Text, View } from 'react-native';

const { width } = Dimensions.get('window');

const StarRating = ({ score }: { score: number }) => {
    const stars = [];
  
    for (let i = 0; i < 5; i++) {
      if (i + 1 <= score) {
        // Full star
        stars.push(<Text key={i} style={styles.star}>★</Text>);
      } else if (i < score && score < i + 1) {
        // Half star
        stars.push(
          <View key={i} style={styles.halfStarContainer}>
            <Text style={styles.starEmpty}>★</Text>
            <View style={styles.halfOverlay}>
              <Text style={styles.star}>★</Text>
            </View>
          </View>
        );
      } else {
        // Empty star
        stars.push(<Text key={i} style={styles.starEmpty}>★</Text>);
      }
    }
  
    return <View style={{ flexDirection: 'row' }}>{stars}</View>;
  };
  

export default function SafetyFlow() {
  const { data: rawData } = useLocalSearchParams();
  let data: any[] = [];
  try {
    const parsed = rawData ? JSON.parse(rawData as string) : [];
    data = [
      {
      "Neighbourhood": "Nieuwmarkt/Lastage",
      "Safety Score": "2.0/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; neighbourhood described with 'stoned' and 'tourists'.",
      "Social Character": "Relaxed, touristy vibe with a hint of laid-back atmosphere."
    },
    {
      "Neighbourhood": "Oostelijke Eilanden/Kadijken",
      "Safety Score": "3.5/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; unusual vibe keywords.",
      "Social Character": "Unclear due to non-descriptive keywords (e.g., emojis of animals)."
    },
    {
      "Neighbourhood": "Grachtengordel-West",
      "Safety Score": "4.0/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No direct safety news; described with long queues, possibly indicating popularity.",
      "Social Character": "Touristy with potentially long wait times for popular attractions."
    },
    {
      "Neighbourhood": "Haarlemmerbuurt",
      "Safety Score": "4.6/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; likened to 'little Venice'.",
      "Social Character": "Charming, possibly serene, akin to a small, picturesque town."
    },
    {
      "Neighbourhood": "Volewijck",
      "Safety Score": "3.5/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; hipster vibe with home buying activity.",
      "Social Character": "Trendy, with an active, possibly affluent, young population."
    },
    {
      "Neighbourhood": "Grachtengordel-Zuid",
      "Safety Score": "3.0/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No direct safety concerns in news; vibrant but potentially disruptive tourist activity.",
      "Social Character": "Lively, tourist-heavy with a party atmosphere."
    },
    {
      "Neighbourhood": "Nieuwendammerham",
      "Safety Score": "3.1/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; active with skate culture.",
      "Social Character": "Youthful, active community with a skate culture influence."
    },
    {
      "Neighbourhood": "Staatsliedenbuurt",
      "Safety Score": "1.0/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "Multiple crime and violence reports indicate a high safety concern.",
      "Social Character": "Unclear due to lack of descriptive vibe keywords; safety concerns predominant."
    },
    {
      "Neighbourhood": "Tuindorp Buiksloot",
      "Safety Score": "3.0/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; described with 'barbed gardens', implying potential neglect.",
      "Social Character": "Uncertain; 'barbed gardens' suggest possible disrepair or security measures."
    },
    {
      "Neighbourhood": "Dapperbuurt",
      "Safety Score": "4.0/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "Mixed signals with no direct safety threats but some incidents reported.",
      "Social Character": "Hip, with a good beer culture, indicating a laid-back, possibly trendy atmosphere."
    },
    {
      "Neighbourhood": "Frederik Hendrikbuurt",
      "Safety Score": "4.1/5.0",
      "Top 3 Safe Places": [],
      "Safety Overview": "No safety data available; cosy square contrasted with hectic traffic.",
      "Social Character": "Mixed vibe of serenity (cosy square) and chaos (hectic traffic)."
    }
].map((n: any) => ({
    neighbourhood: n["Neighbourhood"],
    safety_score: parseFloat(n["Safety Score"]?.split("/")[0]) || 0,
    top_places: n["Top 3 Safe Places"] || [],
    safety_overview: n["Safety Overview"] || "No overview available.",
    social_character: n["Social Character"] || "No description provided."
  }));
} catch (err) {
  console.error("Error parsing or mapping data:", err);
}

return (
  <ScrollView
    horizontal
    pagingEnabled
    style={{ flex: 1, backgroundColor: '#0a1a2f' }}
    showsHorizontalScrollIndicator={false}
  >
    <View style={styles.page}>
      <Text style={styles.title}>Here’s a Safety Review of Your City</Text>
      <Text style={styles.subtitle}>
        Discover your city’s safety score and uncover hidden risks and safe havens!
        With real-time updates from news and crowd-sourced data, this feature gives you the
        power to stay one step ahead and explore with confidence!
      </Text>
      <Text style={styles.subtitleSmall}>Scroll to explore all the neighborhoods!</Text>
    </View>

    {data.map((n: any, index: number) => (
      <View style={styles.page} key={index}>
        <Text style={styles.neighborhoodTitle}>{n.neighbourhood}</Text>
        <Text style={styles.sectionLabel}>Safety Score</Text>
        <Text style={styles.score}>{(n.safety_score ?? 0).toFixed(1)}</Text>
        <StarRating score={n.safety_score ?? 0} />

        <Text style={styles.sectionLabel}>Safety Overview</Text>
        <Text style={styles.description}>{n.safety_overview}</Text>

        <Text style={styles.sectionLabel}>Top 3 Safe Places</Text>
        {(n.top_places.length ? n.top_places : ['No data available']).map((place: string, i: number) => (
          <Text key={i} style={styles.description}>- {place}</Text>
        ))}

        <Text style={styles.sectionLabel}>What are the people like here?</Text>
        <Text style={styles.description}>{n.social_character}</Text>
      </View>
    ))}
  </ScrollView>
);
}

const styles = StyleSheet.create({
page: {
  width,
  padding: 20,
  justifyContent: 'center',
  alignItems: 'flex-start',
},
title: {
  fontSize: 22,
  fontWeight: 'bold',
  color: '#fff',
  textAlign: 'left',
  marginBottom: 12,
},
subtitle: {
  fontSize: 15,
  color: '#ccc',
  marginBottom: 10,
},
subtitleSmall: {
  fontSize: 13,
  color: '#aaa',
  marginTop: 10,
},
neighborhoodTitle: {
  fontSize: 20,
  color: '#fff',
  fontWeight: 'bold',
  marginBottom: 8,
},
score: {
  fontSize: 32,
  color: '#fff',
  fontWeight: 'bold',
  marginBottom: 4,
},
sectionLabel: {
  fontSize: 14,
  fontWeight: '600',
  color: '#fff',
  marginTop: 12,
},
description: {
  fontSize: 13,
  color: '#ccc',
  marginTop: 4,
},
star: {
  color: '#f1c40f',
  fontSize: 20,
  marginRight: 2,
},
starEmpty: {
  color: '#666',
  fontSize: 20,
  marginRight: 2,
},
halfStarContainer: {
    position: 'relative',
  },
  halfOverlay: {
    position: 'absolute',
    overflow: 'hidden',
    width: '50%',
    height: '100%',
    top: 0,
    left: 0,
  },  
});
