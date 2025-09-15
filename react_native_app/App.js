import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  TouchableOpacity,
  ActivityIndicator,
  Animated,
  Dimensions,
} from 'react-native';

const { width } = Dimensions.get('window');

const App = () => {
  const [features, setFeatures] = useState({
    'Rear Traffic Alert': false,
    'Headlight Status': false,
    'Turn Signals': false,
    'Navigation': false,
    'Speed Limits': false,
    'Takeover Alerts': false,
    'Lane Departure': false,
    'Autopilot Status': false,
    'Gear Position': false,
    'Battery Range': false,
    'Speed Display': false,
  });

  const [selectedTheme, setSelectedTheme] = useState('Dark');
  const [statusMessage, setStatusMessage] = useState('Ready');
  const [isSyncing, setIsSyncing] = useState(false);

  const themes = ['Dark', 'Light', 'Nature', 'Cyber'];

  const toggleFeature = (featureName, value) => {
    setFeatures(prev => ({ ...prev, [featureName]: value }));
    setStatusMessage(`${featureName} ${value ? 'enabled' : 'disabled'} (pending sync)`);
  };

  const syncSettings = async () => {
    setIsSyncing(true);
    
    setTimeout(() => {
      setIsSyncing(false);
      const enabledCount = Object.values(features).filter(Boolean).length;
      setStatusMessage(
        enabledCount > 0
          ? `Synced to device - ${enabledCount} features enabled`
          : 'Synced to device - All features disabled'
      );
    }, 1500);
  };

  const selectTheme = (theme) => {
    setSelectedTheme(theme);
    setStatusMessage(`Theme set to ${theme} for target device`);
  };

  const getThemeColor = (theme) => {
    switch (theme) {
      case 'Nature': return '#00C851';
      case 'Cyber': return '#FF4081';
      default: return '#007AFF';
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView}>
        {/* Dynamic Island */}
        <DynamicIsland />

        {/* Header */}
        <Text style={styles.header}>Settings</Text>

        {/* Status Section */}
        <View style={styles.section}>
          <View style={styles.statusRow}>
            <View>
              <Text style={styles.statusTitle}>Your Drive is up to date</Text>
              <Text style={styles.statusSubtitle}>1.1.22</Text>
            </View>
          </View>
        </View>

        {/* Features Section */}
        <View style={styles.section}>
          {Object.entries(features).map(([name, enabled]) => (
            <View key={name} style={styles.featureRow}>
              <Text style={styles.featureText}>{name}</Text>
              <Switch
                value={enabled}
                onValueChange={(value) => toggleFeature(name, value)}
                trackColor={{ false: '#767577', true: '#00C851' }}
                thumbColor={enabled ? '#fff' : '#f4f3f4'}
              />
            </View>
          ))}
          
          <View style={styles.divider} />
          
          <TouchableOpacity style={styles.settingRow}>
            <Text style={styles.featureText}>Navigation settings</Text>
            <Text style={styles.arrow}>›</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.settingRow}>
            <Text style={styles.featureText}>Units</Text>
            <Text style={styles.arrow}>›</Text>
          </TouchableOpacity>
        </View>

        {/* Theme Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Theme</Text>
          <View style={styles.themeGrid}>
            {themes.map((theme) => (
              <TouchableOpacity
                key={theme}
                style={[
                  styles.themeButton,
                  {
                    backgroundColor: selectedTheme === theme
                      ? getThemeColor(theme)
                      : '#38383A'
                  }
                ]}
                onPress={() => selectTheme(theme)}
              >
                <Text style={styles.themeButtonText}>{theme}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Sync Button */}
        <View style={styles.syncSection}>
          <TouchableOpacity
            style={[styles.syncButton, { opacity: isSyncing ? 0.6 : 1 }]}
            onPress={syncSettings}
            disabled={isSyncing}
          >
            {isSyncing && <ActivityIndicator color="#fff" style={styles.spinner} />}
            <Text style={styles.syncButtonText}>
              {isSyncing ? 'Syncing...' : 'Sync Settings'}
            </Text>
          </TouchableOpacity>
          
          <Text style={styles.statusText}>{statusMessage}</Text>
        </View>
      </ScrollView>
    </View>
  );
};

const DynamicIsland = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const animatedValue = new Animated.Value(isExpanded ? 1 : 0);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
    Animated.timing(animatedValue, {
      toValue: isExpanded ? 0 : 1,
      duration: 300,
      useNativeDriver: false,
    }).start();
  };

  const animatedWidth = animatedValue.interpolate({
    inputRange: [0, 1],
    outputRange: [120, 200],
  });

  return (
    <TouchableOpacity onPress={toggleExpanded} style={styles.dynamicIslandContainer}>
      <Animated.View style={[styles.dynamicIsland, { width: animatedWidth }]}>
        {isExpanded ? (
          <Text style={styles.dynamicIslandText}>HUD Control Active</Text>
        ) : (
          <View style={styles.dynamicIslandDot} />
        )}
      </Animated.View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  scrollView: {
    flex: 1,
    paddingTop: 50,
  },
  dynamicIslandContainer: {
    alignItems: 'center',
    marginVertical: 10,
  },
  dynamicIsland: {
    height: 32,
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  dynamicIslandText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  dynamicIslandDot: {
    width: 6,
    height: 6,
    backgroundColor: '#00C851',
    borderRadius: 3,
  },
  header: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginHorizontal: 20,
    marginVertical: 20,
  },
  section: {
    backgroundColor: '#1C1C1E',
    marginHorizontal: 20,
    marginVertical: 10,
    borderRadius: 16,
    padding: 16,
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusTitle: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  statusSubtitle: {
    color: '#8E8E93',
    fontSize: 12,
    marginTop: 2,
  },
  featureRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  featureText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  divider: {
    height: 1,
    backgroundColor: '#38383A',
    marginVertical: 8,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  arrow: {
    color: '#8E8E93',
    fontSize: 20,
    fontWeight: 'bold',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 15,
  },
  themeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  themeButton: {
    width: (width - 80) / 2,
    height: 38,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  themeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  syncSection: {
    paddingHorizontal: 20,
    paddingVertical: 20,
  },
  syncButton: {
    backgroundColor: '#007AFF',
    height: 52,
    borderRadius: 14,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  spinner: {
    marginRight: 10,
  },
  syncButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  statusText: {
    color: '#8E8E93',
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 15,
  },
});

export default App;