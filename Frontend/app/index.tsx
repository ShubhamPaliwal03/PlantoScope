import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Image, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router'
import * as FileSystem from 'expo-file-system'

const App = () => {

  const router = useRouter();

  const [imageUri, setImageUri] = useState<string | null>(null);
  const [storedImagePath, setStoredImagePath] = useState<string | null>(null);

  // request permissions on app start

  useEffect(() => {

    (async () => {

      const { status: galleryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();

      if (galleryStatus !== 'granted' || cameraStatus !== 'granted') {

        Alert.alert('Permission Denied', 'Please enable camera and media permissions in settings.');
      }

    })();

  }, []);

  // function to save new image (set image uri, save it into async storage, and delete the old image)

  const saveNewImage = async (result: ImagePicker.ImagePickerResult) => {

    if (!result.canceled) {

        // set the image uri
    
        setImageUri(result?.assets[0]?.uri);
    
        // generate a storage path with a new file name to prevent caching issues
    
        const newStoredImagePath = `${FileSystem.documentDirectory}plant_image_${Date.now()}.jpg`;
        
        // save the new image into async storage
    
        await FileSystem.copyAsync({ from: result?.assets[0]?.uri, to: newStoredImagePath });
        
        // delete the old (previous) image
    
        if (storedImagePath !== null) {
    
            await FileSystem.deleteAsync(storedImagePath, { idempotent: true });
        }
    
        setStoredImagePath(newStoredImagePath);
    }
  }

  // function to pick an image

  const pickImage = async () => {

    let result = await ImagePicker.launchImageLibraryAsync({

      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });
    
    saveNewImage(result);
  };

  // function to capture an image

  const captureImage = async () => {

    let result = await ImagePicker.launchCameraAsync({

      allowsEditing: true,
      quality: 1,
    });

    saveNewImage(result);
  };

  const analyzeImage = async () => {

      if (!imageUri) return;

      const formData = new FormData();

      formData.append('file', {

        uri: imageUri,
        name: 'plant_image.jpg',
        type: 'image/jpeg',

      } as any);

      try {

        // https://plantoscope-backend.onrender.com/predict
        // https://web-production-82a2.up.railway.app/predict
        
        const res = await fetch('https://plantoscope-backend.onrender.com/predict', {

          method: 'POST',
          headers: {
            'x-api-key': 'b5b937fc8d2017619b03f36fb6c184bf42fb28f9da200410eca64e34e63a528c'
          },
          body: formData,
        });

        const data = await res.json();

        if (res.ok) {

          router.push({
            
            pathname: '/result',
            params: {
              ...data,
              storedImagePath
            }
          });

        } else {

          console.error()
          alert('Something went wrong!\nPlease try again.')
        }
      }
      catch(err) {

        console.error(err);
        alert('Failed to fetch result.\nMake sure you are connected to the internet.');
      }
  }

  return (
    <LinearGradient colors={['#4CAF50', '#000000']} style={{ flex: 1, justifyContent: 'space-around', alignItems: 'center', padding: 20, flexDirection: 'column', backgroundColor: '#000000' }}>
      <Text style={{ fontSize: 30, fontWeight: 'bold', color: '#fff' }}>Plantoscope ☘️</Text>
      {imageUri ? (
        <Image source={{ uri: imageUri }} style={{ width: 250, height: 250, borderRadius: 15, marginBottom: 20 }} />
      ) : (
        <Text style={{ color: 'white', fontSize: 16, marginBottom: 20 }}>No image selected</Text>
      )}
      <View>
        <TouchableOpacity onPress={pickImage} style={{ backgroundColor: 'white', flexDirection: 'row', alignItems: 'center', padding: 12, borderRadius: 10, marginBottom: 10 }}>
          <Ionicons name="image" size={24} color="#4CAF50" style={{ marginRight: 10 }} />
          <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#4CAF50' }}>Select from Gallery</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={captureImage} style={{ backgroundColor: 'white', flexDirection: 'row', alignItems: 'center', padding: 12, borderRadius: 10 }}>
          <Ionicons name="camera" size={24} color="#4CAF50" style={{ marginRight: 10 }} />
          <Text style={{ fontSize: 16, fontWeight: 'bold', color: '#4CAF50' }}>Capture from Camera</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity onPress={analyzeImage} style={{ backgroundColor: 'white', flexDirection: 'row', alignItems: 'center', padding: 12, borderRadius: 10, marginTop: 10, gap: 10 }}>
        {/* <Ionicons name="sparkles-sharp" size={24} color="rgb(0, 122, 255);" style={{ marginRight: 10 }} /> */}
        <Image source={require('../assets/images/ai_analysis_logo.png')} style={{ width: 30, height: 30 }}></Image>
        <Text style={{ fontSize: 16, fontWeight: 'bold', color: 'black' }}>Analyze using Planto AI</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
};

export default App;