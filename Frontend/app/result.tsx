import { Text, Image, ScrollView } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';

export default function ResultScreen() {

  const { plant_type, disease_name, cause, cure, storedImagePath } = useLocalSearchParams();

  return (
    <LinearGradient colors={['#4CAF50', '#000000']}>
      <ScrollView style={{ padding:20 }}>
        <Text style={{ fontSize: 28, fontWeight: 'bold', color: 'white', marginTop: 40, marginBottom: 40 }}>
          AI Diagnosis Result
        </Text>
        { storedImagePath && (
          
          <Image
            source={{ uri: storedImagePath as string }}
            style={{ width: '100%', height: 250, borderRadius: 12, marginBottom: 40 }}
            resizeMode='stretch'
          />
        )}

        <Text style={{ fontSize: 20, fontWeight:'bold', marginBottom: 10, color: 'white' }}>Plant Type:</Text>
        <Text style={{ fontSize: 18, marginBottom: 30, color: 'white' }}>{ plant_type }</Text>

        <Text style={{ fontSize: 20, fontWeight:'bold', marginBottom: 10, color: 'white' }}>Disease Name:</Text>
        <Text style={{ fontSize: 18, marginBottom: 30, color: 'white' }}>{ disease_name }</Text>

        { cause !== '' && (
          <>
            <Text style={{ fontSize: 20, fontWeight:'bold', marginBottom: 10, color: 'white' }}>Cause:</Text>
            <Text style={{ fontSize: 18, marginBottom: 30, color: 'white' }}>{ cause }</Text>
          </>
        )}

        { cure !== '' && (
          <>
            <Text style={{ fontSize: 20, fontWeight:'bold', marginBottom: 10, color: 'white' }}>Cure:</Text>
            <Text style={{ fontSize: 18, color: 'white' }}>{ cure }</Text>
          </>
        )}
      </ScrollView>
    </LinearGradient>
  )
};