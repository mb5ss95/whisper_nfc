import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


# storageBucket': 'project-83e1e.appspot.com', 'mystory-c28b0.appspot.com'
cred = credentials.Certificate('/home/pi/whisper/key/mykey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mystory-c28b0.appspot.com'
})


bucket = storage.bucket()

'''
temp = bucket.list_blobs()

for i in temp:
    print(dir(i))

'''
blob = bucket.blob("my_name2.mp3")

#blob.upload_from_filename("/home/pi/test/st.mp3")
#blob.upload_from_filename("/home/pi/whisper/mp3/cheerup.mp3", checksum="md5")

#time.sleep(5)

#blob.download_to_filename("/home/pi/my_name2.mp3", checksum="md5")
temp = blob.download_as_bytes(checksum="md5")
print(temp)


# 'bucket' is an object defined in the google-cloud-storage Python library.
# See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# for more details.

