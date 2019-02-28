import pyaes
import configparser


class Encryption:
    def __init__(self,pobj_config_parser):    
        try:              
            
            self.gstr_sender_ID = str(pobj_config_parser['General']['sender_ID'])
            self.gstr_password = str(pobj_config_parser['General']['password'])
    
        except:
            raise
        
    def encode(self,pobj_data,pobj_password):
        
        '''
        
        method description :
            This method is used to encrypt data with encryption key.
            
        '''
        key = pobj_password
        key = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)    
        ciphertext = aes.encrypt(pobj_data)
        return ciphertext
    
    def decode(self,pobj_data,pobj_password):
        
        '''
        
        method description :
            This method is used to decrypt data with decryption key.
            
        '''
        key = pobj_password
        key = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)
        decrypted = aes.decrypt(pobj_data).decode("utf-8")
        return decrypted
if __name__ == '__main__':
    try:             
        #=======================================================================
        # reading the config file and find out logger path
        #======================================================================= 
        lobj_config_parser = configparser.ConfigParser() 
        lobj_config_parser.read('config.ini')
        
        
        # create object of Encryption
        gobj_Encryption=Encryption(lobj_config_parser)
        
        key="This_key_for_demo_purposes_only!"
        ENC = gobj_Encryption.encode(gobj_Encryption.gstr_password,key)
        ENC1 = gobj_Encryption.encode(gobj_Encryption.gstr_sender_ID,key)
        print(ENC)
        print(ENC1)
        dec = gobj_Encryption.decode(ENC,key)
        dec1 = gobj_Encryption.decode(ENC1,key)
        print(dec)
        print(dec1)
        
        #with open('file.enc', 'wb') as f:
         #   f.write(b'abcdefg')

        
        cfgfile = open("config.ini",'w')
        #update existing value in config.ini
        lobj_config_parser.set('General','sender_ID',str(ENC1))
        lobj_config_parser.set('General','password',str(ENC))
        
        lobj_config_parser.write(cfgfile) 
        
    except Exception as e:
        print(str(e))