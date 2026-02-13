import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, StatusBar, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { useChat } from '../hooks/useChat';

export default function VoiceChatScreen() {
  const [isMuted, setIsMuted] = React.useState(false);
  const [statusText, setStatusText] = React.useState('正在聆听...');
  const [cameraEnabled, setCameraEnabled] = React.useState(false);
  const [isInteractive, setIsInteractive] = React.useState(false);
  const [facing, setFacing] = React.useState<'front' | 'back'>('front');
  const [permission, requestPermission] = useCameraPermissions();
  
  const { clearHistory } = useChat();

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
    
    const newCameraState = !cameraEnabled;
    setCameraEnabled(newCameraState);
    setStatusText(newCameraState ? '已启动摄像头' : '正在聆听...');
  };

  const toggleCameraFacing = () => {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  };

  const handleInteractivePress = () => {
    setIsInteractive(!isInteractive);
    setStatusText(isInteractive ? '正在聆听...' : '已开启共享屏幕');
  };

  const handleClearChat = async () => {
    Alert.alert(
      '新建会话',
      '确定要清空当前对话历史吗？',
      [
        {
          text: '取消',
          style: 'cancel',
        },
        {
          text: '确定',
          onPress: async () => {
            try {
              await clearHistory();
              setStatusText('已创建新会话');
            } catch (error) {
              setStatusText('新建会话失败');
              console.error('清除对话失败:', error);
            }
          },
        },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle={cameraEnabled ? 'light-content' : 'dark-content'} />
      
      {cameraEnabled ? (
        <CameraView style={styles.cameraFullscreen} facing={facing} />
      ) : (
        <LinearGradient
          colors={['#FFE5F0', '#E8F4FF']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={styles.gradient}
        />
      )}

      {cameraEnabled && (
        <TouchableOpacity 
          style={styles.flipButton}
          onPress={toggleCameraFacing}
        >
          <Ionicons name="camera-reverse" size={24} color="#FFF" />
        </TouchableOpacity>
      )}

      <View style={styles.contentLayer}>
        <View style={styles.statusContainer}>
          <Text style={[styles.statusText, cameraEnabled && styles.statusTextLight]}>{statusText}</Text>
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
                style={styles.circleButton}
                onPress={handleClearChat}
              >
                <Ionicons 
                  name="add-circle-outline" 
                  size={28} 
                  color="#333" 
                />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>新建会话</Text>
            </View>
            
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
              <TouchableOpacity 
                style={[styles.circleButton, isInteractive && styles.circleButtonActive]}
                onPress={handleInteractivePress}
              >
                <MaterialIcons 
                  name="screen-share" 
                  size={28} 
                  color={isInteractive ? '#FFF' : '#333'} 
                />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>共享屏幕</Text>
            </View>
            
            <View style={styles.buttonWrapper}>
              <TouchableOpacity 
                style={[styles.circleButton, cameraEnabled && styles.circleButtonActive]} 
                onPress={toggleCamera}
              >
                <Ionicons 
                  name="videocam" 
                  size={28} 
                  color={cameraEnabled ? '#FFF' : '#333'} 
                />
              </TouchableOpacity>
              <Text style={[styles.buttonLabel, cameraEnabled && styles.buttonLabelLight]}>摄像头</Text>
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
});
