import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';
import { CameraView, useCameraPermissions } from 'expo-camera';

export default function App() {
  const [isMuted, setIsMuted] = React.useState(false);
  const [statusText, setStatusText] = React.useState('正在聆听...');
  const [cameraEnabled, setCameraEnabled] = React.useState(false);
  const [facing, setFacing] = React.useState<'front' | 'back'>('front');
  const [permission, requestPermission] = useCameraPermissions();

  // Demo metrics (placeholders)
  const [metrics, setMetrics] = React.useState({ asr: 180, ttft: 420, ttsBuf: 350 });
  React.useEffect(() => {
    const t = setInterval(() => {
      setMetrics(m => ({
        asr: Math.max(100, Math.min(800, Math.round(m.asr + (Math.random()-0.5)*40))),
        ttft: Math.max(200, Math.min(2000, Math.round(m.ttft + (Math.random()-0.5)*80))),
        ttsBuf: Math.max(0, Math.min(5000, Math.round(m.ttsBuf + (Math.random()-0.5)*120))),
      }));
    }, 1500);
    return () => clearInterval(t);
  }, []);

  const handleMicPress = () => {
    setIsMuted(!isMuted);
    setStatusText(isMuted ? '正在聆听...' : '已静音');
  };

  const toggleCamera = async () => {
    if (!permission) {
      return;
    }
    
    if (!permission.granted) {
      const result = await requestPermission();
      if (!result.granted) {
        return;
      }
    }
    
    setCameraEnabled(!cameraEnabled);
  };

  const toggleCameraFacing = () => {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle={cameraEnabled ? 'light-content' : 'dark-content'} />
      
      {cameraEnabled ? (
        <CameraView style={styles.cameraFullscreen} facing={facing}>
          <TouchableOpacity 
            style={styles.flipButton}
            onPress={toggleCameraFacing}
          >
            <Ionicons name="camera-reverse" size={24} color="#FFF" />
          </TouchableOpacity>
        </CameraView>
      ) : (
        <LinearGradient
          colors={['#FFE5F0', '#E8F4FF']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.gradient}
        />
      )}

      <View style={styles.contentLayer}>
        <View style={styles.statusContainer}>
          <Text style={[styles.statusText, cameraEnabled && styles.statusTextLight]}>{statusText}</Text>
        </View>

        <View style={styles.debugCard}>
          <Text style={styles.debugTitle}>调试</Text>
          <Text style={styles.debugItem}>ASR: {metrics.asr}ms</Text>
          <Text style={styles.debugItem}>TTFT: {metrics.ttft}ms</Text>
          <Text style={styles.debugItem}>TTS: {metrics.ttsBuf}ms</Text>
        </View>

        <View style={styles.centerContainer}>
          <View style={styles.dotsContainer}>
            <View style={styles.dot} />
            <View style={styles.dot} />
            <View style={styles.dot} />
          </View>
          <Text style={[styles.centerText, cameraEnabled && styles.centerTextLight]}>你可以开始说话</Text>
        </View>

        <View style={styles.bottomContainer}>
          <View style={styles.buttonRow}>
            <View style={styles.buttonWrapper}>
              <TouchableOpacity 
                style={[styles.circleButton, isMuted && styles.circleButtonMuted]} 
                onPress={handleMicPress}
              >
                <Ionicons 
                  name={isMuted ? "mic-off" : "mic"} 
                  size={28} 
                  color={isMuted ? '#FFF' : '#333'} 
                />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>录音</Text>
            </View>
            
            <View style={styles.buttonWrapper}>
              <TouchableOpacity style={styles.circleButton}>
                <MaterialIcons name="screen-share" size={28} color="#333" />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>共享屏幕</Text>
            </View>
            
            <View style={styles.buttonWrapper}>
              <TouchableOpacity 
                style={[styles.circleButton, styles.circleButtonLarge, cameraEnabled && styles.circleButtonActive]} 
                onPress={toggleCamera}
              >
                <Ionicons name="videocam" size={32} color={cameraEnabled ? '#FFF' : '#333'} />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>摄像头</Text>
            </View>
            
            <View style={styles.buttonWrapper}>
              <TouchableOpacity style={styles.circleButton}>
                <Ionicons name="close" size={32} color="#FF6B6B" />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>退出</Text>
            </View>
          </View>

          </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    ...StyleSheet.absoluteFillObject,
  },
  cameraFullscreen: {
    ...StyleSheet.absoluteFillObject,
  },
  contentLayer: {
    ...StyleSheet.absoluteFillObject,
  },
  flipButton: {
    position: 'absolute',
    top: 60,
    right: 20,
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  statusContainer: {
    paddingHorizontal: 40,
    paddingTop: 80,
  },
  statusText: {
    fontSize: 32,
    color: '#666',
    fontWeight: '300',
  },
  statusTextLight: {
    color: '#FFF',
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 3,
  },
  debugCard: {
    position: 'absolute',
    right: 20,
    bottom: 200,
    backgroundColor: 'rgba(50, 50, 50, 0.85)',
    borderRadius: 12,
    padding: 12,
    minWidth: 120,
  },
  debugTitle: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  debugItem: {
    color: '#E0E0E0',
    fontSize: 12,
    marginBottom: 4,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingBottom: 100,
  },
  dotsContainer: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 16,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#999',
  },
  centerText: {
    fontSize: 18,
    color: '#666',
    fontWeight: '400',
  },
  centerTextLight: {
    color: '#FFF',
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 3,
  },
  bottomContainer: {
    paddingBottom: 40,
    alignItems: 'center',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'flex-end',
    marginBottom: 16,
  },
  buttonWrapper: {
    alignItems: 'center',
    marginHorizontal: 8,
  },
  circleButton: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  circleButtonLarge: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#FFFFFF',
  },
  circleButtonActive: {
    backgroundColor: '#4A90E2',
  },
  circleButtonMuted: {
    backgroundColor: '#EF4444',
  },
  buttonLabel: {
    marginTop: 6,
    fontSize: 12,
    color: '#666',
  },
  buttonLabelLight: {
    color: '#FFF',
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 3,
  },
  bottomText: {
    marginTop: 8,
    fontSize: 12,
    color: '#999',
  },
  bottomTextLight: {
    color: '#FFF',
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 3,
  },
});
