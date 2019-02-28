from logger.LoggerError import LoggerError
from logger.logger import Logger
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


import configparser
import os
import zipfile
import smtplib
import argparse
from encrypt1 import Encryption


class mail():
    def __init__(self, pobj_logger, pobj_config_parser, pobj_args):
        
        try:         
            
            #===================================================================
            # create object of other classes
            #===================================================================
            self.gobj_logger = pobj_logger
            
            self.gstr_recepient=pobj_args.recepient
            self.gstr_subject=str(pobj_args.subject)
            self.gstr_directory_of_files=pobj_args.directory_of_files
            
            self.gobj_Encryption = Encryption(pobj_config_parser)
            
            self.gstr_name_of_destination_archive = str(pobj_config_parser['General']['name_of_destination_archive'])
            self.gstr_server = str(pobj_config_parser['General']['server'])
            self.gint_port=int(pobj_config_parser['General']['port'])
            self.gstr_sender_ID = eval(pobj_config_parser['General']['sender_ID'])
            self.gstr_password = eval(pobj_config_parser['General']['password'])
            self.gstr_lbol_isgmail = str(pobj_config_parser['General']['lbol_isgmail'])
                             
        except Exception:
            print("CONFIGURATION ERROR")
            pobj_logger.info("Method Name: Constructor of Pipeline\n",exc_info=True)
            raise SystemExit
    

 
    def zip(self,pstr_src, pstr_dst):
    
        '''
        
        method description :
            This method is used to create zip file.
            
        '''

        try:
            zf = zipfile.ZipFile("%s.zip" % (pstr_dst), "w")
            for lstr_dirname, lstr_subdirs, lstr_files in os.walk(pstr_src):
                zf.write(lstr_dirname)
                for lstr_filename in lstr_files:
                    zf.write(os.path.join(lstr_dirname, lstr_filename))
            zf.close()
        except:
            pass 
    

    def sendMsg(self):
    
        '''
        
        method description :
            This method is used to send a mail with attachment of zip file.
            
        '''
        subject = self.gstr_subject
        recepient = self.gstr_recepient
        self.gstr_sender_ID = self.gobj_Encryption.decode(self.gstr_sender_ID, "This_key_for_demo_purposes_only!")
        sender = self.gstr_sender_ID
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recepient
         
        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(self.gstr_name_of_destination_archive+ ".zip", "rb").read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=\"%s.zip\"" % (self.gstr_name_of_destination_archive))
        msg.attach(part)
         
        smtp = smtplib.SMTP(self.gstr_server, self.gint_port)
        if self.gstr_lbol_isgmail:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            
            #self.gstr_sender_ID = self.gobj_Encryption.decode(self.gstr_sender_ID, "This_key_for_demo_purposes_only!")
            self.gstr_password = self.gobj_Encryption.decode(self.gstr_password, "This_key_for_demo_purposes_only!")
            smtp.login(self.gstr_sender_ID,self.gstr_password)
            
            sender = self.gstr_sender_ID
            
            smtp.sendmail(sender, recepient, msg.as_string())
            smtp.close()

    def main(self):
        try:      
            self.gstr_directory_of_files = self.gstr_directory_of_files.split("/")       
            self.zip(self.gstr_directory_of_files[-1],self.gstr_name_of_destination_archive)
            #print(self.gstr_directory_of_files[-1],self.gstr_name_of_destination_archive)
            self.sendMsg()
            print ("Message sent successfuly")
        except Exception:
            self.gobj_logger.info("Method Name: main() method of Pipeline\n")
            raise     
     

def parse_args(pobj_logger):

    '''
        
        method description :
            This method is used to create argument parser.
        output : 
            argument parser
    '''
    try:
        #=======================================================================
        # adding arguments
        #=======================================================================
        lobj_argparse = argparse.ArgumentParser()  
        
        lobj_argparse.add_argument('--recepient',required=True) 
        lobj_argparse.add_argument('--subject',required=True) 
        lobj_argparse.add_argument('--directory_of_files',required=True) 
        
        lobj_args = lobj_argparse.parse_args()
        
        return lobj_args
    
    except SystemExit:
        print("CONFIGURATION ERROR")
        pobj_logger.info("Method Name: parse_args(self)\n"
                    +"argument --input_path is not given or unrecognized")
        raise    
        
    except Exception:
        pobj_logger.info("Method Name: parse_args(self)\n")
        raise 
 
              
if __name__ == '__main__':
    try:             
        #=======================================================================
        # reading the config file and find out logger path
        #======================================================================= 
        lobj_config_parser = configparser.ConfigParser() 
        lobj_config_parser.read('config.ini')     

        # create object of logger
        lobj_logger = Logger().logger
        
        # create argument parser
        lobj_args = parse_args(lobj_logger)
        
        # create object of mail
        gobj_mail = mail(lobj_logger, lobj_config_parser, lobj_args)
        
        # call main function inside mail class
        gobj_mail.main() 
       
    except LoggerError as l:
        print(l)
    except Exception:
        print("ERROR")
        lobj_logger.error("Exception Raised", exc_info=True)
        
        
