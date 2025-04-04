from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi import Message, ThreadType, Mention, MessageStyle, MultiMsgStyle
from concurrent.futures import ThreadPoolExecutor
import time
from time import sleep 
from datetime import datetime
import threading
import random
import subprocess
import json
import requests
from Crypto.Cipher import AES
import base64
import logging
def Tcp_Focx():
    try:
        with open('admin.json', 'r') as adminvip:
            adminzalo = json.load(adminvip)
            return set(adminzalo.get('idadmin', []))
    except FileNotFoundError:
        return set()
idadmin = Tcp_Focx()
class QuynhAnh(ZaloAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spamming = False
        self.spam_thread = None
        self.spammingvip = False
        self.spam_threadvip = None
        self.reo_spamming = False
        self.reo_spam_thread = None
        self.idnguoidung = ['207754413506549669']
        self.excluded_user_ids = []
        self.call_running = False
        self.successful_call = 0
        self.todo_running = False
        self.successful_todos = 0
        self.thread_pool = ThreadPoolExecutor(max_workers=100000000)
        self.imei = kwargs.get('imei')
        self.session_cookies = kwargs.get('session_cookies')
        self.secret_key = self.getSecretKey()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "origin": "https://chat.zalo.me",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Accept-Encoding": "gzip",
            "referer": "https://chat.zalo.me/",
            "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        }
        self.headers2 = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "origin": "https://chat.zalo.me",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Accept-Encoding": "gzip",
            "referer": "https://chat.zalo.me/",
            "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def zalo_encode(self, params):
        try:
            key = base64.b64decode(self.secret_key)
            iv = bytes.fromhex("00000000000000000000000000000000")
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = json.dumps(params).encode()
            padded_plaintext = self._pad(plaintext, AES.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)
            return base64.b64encode(ciphertext).decode()
        except Exception as e:
            logging.error(f'Encoding error: {e}')
            return None

    def _pad(self, data, block_size):
        padding_size = block_size - len(data) % block_size
        return data + bytes([padding_size] * padding_size)
    
    def StartCall(self, target_id, call_count):
        def _run_call():
            self.call_running = True
            futures = []
            for i in range(call_count):
                if not self.call_running:
                    break
                callid_random = self.TaoIDCall()
                futures.append(
                    self.thread_pool.submit(
                        self.call,
                        target_id,
                        callid_random
                    )
                )
                time.sleep(0)
            for future in futures:
                future.result()
            completion_message = f"𝐒𝐩𝐚𝐦 𝐒𝐮𝐜𝐜𝐞𝐬𝐬 𝐅𝐮𝐥𝐥 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 {self.successful_call} / {call_count} 𝐂𝐚𝐥𝐥"
            print(completion_message)
            self.call_running = False
        threading.Thread(target=_run_call, daemon=True).start()
    def TaoIDCall(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(9)])
    def call(self, target_id, callid_random):
        payload = {
            "params": {
                "calleeId": target_id,
                "callId": callid_random,
                "codec": "[]\n",
                "typeRequest": 1,
                "imei": self.imei
            }
        }
        payload["params"] = self.zalo_encode(payload["params"])
        call_url1 = 'https://voicecall-wpa.chat.zalo.me/api/voicecall/requestcall?zpw_ver=646&zpw_type=24'
        response = requests.post(call_url1, params=payload["params"], data=payload, headers=self.headers, cookies=self.session_cookies)
        json_data = json.loads(response.text)
        call_payload = {
                "params": {
                    'calleeId': target_id,
                    'rtcpAddress': "171.244.25.88:4601",
                    'rtpAddress': "171.244.25.88:4601",
                    'codec': '[{"dynamicFptime":0,"frmPtime":20,"name":"opus/16000/1","payload":112}]\n',
                    'session': callid_random,
                    'callId': callid_random,
                    'imei': self.imei,
                    'subCommand': 3
                }
        }
        call_payload["params"] = self.zalo_encode(call_payload["params"])
        call_url2 = 'https://voicecall-wpa.chat.zalo.me/api/voicecall/request?zpw_ver=646&zpw_type=24'
        response = requests.post(call_url2, params=call_payload["params"], data=call_payload, cookies=self.session_cookies)

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print(f"""\033[1;36mMessage: \033[32m{message} \n\033[1;36mUid User:\033[31m {author_id} \n\033[1;36mUid Group:\033[33m {thread_id}\033[0m\n""")
        try:
            content = message_object.content if message_object and hasattr(message_object, 'content') else ""
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    pass
            if isinstance(content, dict):
                action = content.get('action')
                params = content.get('params')
                if action == 'recommened.user' and params:
                    reply_id = str(params)
                    reply_message = Message(text=reply_id)
                    self.replyMessage(
                        reply_message,
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )  
                    return
            if not isinstance(message, str):
                return
        except Exception as content_error:
            logging.warning(f"Lỗi trong onMessage: {content_error}")
        if not isinstance(message, str):
            print(f"{type(message)}")
            return
        if message.startswith("Menu"):
           self.replyMessage(Message(text='''
> ├> ʙᴏᴛ ᴠɪᴘ ᴏꜰꜰ ᴅᴜᴏɴɢ ɴɢᴏᴄ ᴄᴏᴅᴇʀ
> ├ ᴀʟʟ: ᴛᴀɢ ᴀʟʟ ᴛᴇxᴛ ɴᴏ ᴋᴇʏ
> ├ ᴏꜰꜰ: ʙᴏᴛ ꜱᴛᴏᴘ ᴡᴏʀᴋɪɴɢ 
> ├ ʀᴇᴏꜱᴘ: ꜱᴘᴀᴍ ᴛᴀɢ ᴍᴇᴍʙᴇʀ 
> ├ ꜱᴛᴏᴘʀ: ꜱᴛᴏᴘ ᴛᴀɢ ꜱᴘᴀᴍ
> ├> ᴏᴛʜᴇʀꜱ ꜰᴜɴᴄᴛɪᴏɴꜱ ᴏꜰ ʙᴏᴛ
> ├ ɪɴꜰᴏ: ᴘʀᴏꜰɪʟᴇ ᴜɪᴅ ᴜꜱᴇʀ - ᴜɪᴅ ɢʀᴏᴜᴘ - ɴᴀᴍᴇ ᴜꜱᴇʀ
> ├ ꜱᴘᴀᴍ: ꜱᴘᴀᴍ ᴍᴇꜱꜱᴀɢᴇ 
> ├ ꜱᴛᴏᴘꜱᴘᴀᴍ: ꜱᴛᴏᴘ ꜱᴘᴀᴍ ᴍᴇꜱꜱᴀɢᴇ 
> ├ ꜱᴘᴀᴍᴠɪᴘ: ꜱᴘᴀᴍ ᴍᴇꜱꜱᴀɢᴇ ᴀɴᴅ ᴛᴀɢ ᴀʟʟ
> ├ ꜱᴛᴏᴘꜱᴘᴀᴍᴠɪᴘ: ꜱᴛᴏᴘ ꜱᴘᴀᴍ ᴍᴇꜱꜱᴀɢᴇ ᴀɴᴅ ᴛᴀɢ ᴀʟʟ
> ├> ʙᴏᴛ ᴢᴀʟᴏ - ᴅᴜᴏɴɢ ɴɢᴏᴄ
            '''), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Flood"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo.get('idadmin', []))

            if author_id not in idadmin:
                return

            args = message.strip().split()
            if len(args) == 1:
                self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙁𝙡𝙤𝙤𝙙 𝙊𝙛𝙛\n𝙁𝙡𝙤𝙤𝙙 𝙊𝙣 𝘿𝙚𝙡𝙖𝙮'), thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return

            if args[1].lower() == "off":
                self.dungFlood()  
                self.replyMessage(Message(text='✅ 𝙎𝙩𝙤𝙥 𝙁𝙡𝙤𝙤𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return

            if args[1].lower() == "on":
                if len(args) < 3 or not args[2].isdigit():
                    self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙁𝙡𝙤𝙤𝙙 𝙊𝙛𝙛\n𝙁𝙡𝙤𝙤𝙙 𝙊𝙣 𝘿𝙚𝙡𝙖𝙮'), thread_id=thread_id, thread_type=thread_type, ttl=30000)
                    return

                try:
                    delay = float(args[2].strip())
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 𝙃𝙤𝙬 𝙏𝙤 𝘿𝙚𝙡𝙖𝙮 ?'), thread_id=thread_id, thread_type=thread_type, ttl=30000)
                        return

                    with open('Quyt.txt', 'r') as file:
                        flood_text = file.readlines()
                        flood_text = [line.strip() for line in flood_text if line.strip()]  # Xóa dòng trống

                    group = self.fetchGroupInfo(thread_id)
                    group_info = group.get("gridInfoMap", {}).get(thread_id, {})
                    mem_ver_list = group_info.get('memVerList', [])
                    cleaned_list = [item.replace('_0', '') for item in mem_ver_list]

                    mentions = [Mention(user_id, offset=0, length=3000, auto_format=False) for user_id in cleaned_list]
                    cc = MultiMention(mentions)

                    while True:
                        word = random.choice(flood_text)  # Chọn nội dung spam ngẫu nhiên
                        self.send(Message(text=str(word), mention=cc), thread_id, thread_type)
                        time.sleep(delay)

                except ValueError:
                    self.replyMessage(Message(text='🚫 𝙄𝙣𝙘𝙤𝙧𝙧𝙚𝙘𝙩 𝙐𝙨𝙖𝙜𝙚 !\n𝙁𝙡𝙤𝙤𝙙 𝙊𝙛𝙛\n𝙁𝙡𝙤𝙤𝙙 𝙊𝙣 𝘿𝙚𝙡𝙖𝙮'), thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith('C'):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            parts = message.split(" ", 1)
            if len(parts) < 2:
                client.replyMessage(
                    Message(text="⚠️ Vui lòng cung cấp UID nhóm !"), 
                    message_object, thread_id, thread_type
                )
                return
            group_id = parts[1].strip()
            self.send(Message(text='Flood on 0'), thread_id=group_id, thread_type=ThreadType.GROUP)
        elif message.startswith("Join"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            try:
                parts = message.split(" ", 1)
                if len(parts) < 2:
                    client.replyMessage(
                        Message(text="⚠️ Vui lòng cung cấp link nhóm !"), 
                        message_object, thread_id, thread_type
                    )
                    return
                url = parts[1].strip()
                if not url.startswith("https://zalo.me/"):
                    client.replyMessage(
                        Message(text="⛔ Link không hợp lệ! Link phải bắt đầu bằng https://zalo.me/"), 
                        message_object, thread_id, thread_type
                    )
                    return
                join_result = self.joinGroup(url)
                if not join_result:
                   self.replyMessage(Message(text='Không thể tham gia nhóm'), thread_id=thread_id, thread_type=thread_type)
                group_info = self.getiGroup(url)
                if not isinstance(group_info, dict) or 'groupId' not in group_info:
                    raise ZaloAPIException("Không thể lấy thông tin nhóm")
                group_id = group_info['groupId']
                print(f"C {group_id}")
            except Exception as e:
                   self.replyMessage(
                       Message(text=f"❌ Lỗi: {str(e)}"),
                       message_object, thread_id, thread_type
                   )
        elif message.startswith("AllCD"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            try:
                parts = message.split(" ", 1)
                if len(parts) < 2:
                    self.replyMessage(Message(text="🚫 𝑈𝑠𝑒:\nAllV3 𝑡𝑒𝑥𝑡_𝑎𝑙𝑙"), 
                                     message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                    return  
                text_all = parts[1].strip()
                mentions = []
                group = self.fetchGroupInfo(thread_id)
                group_info = group.gridInfoMap[thread_id]
                mem_ver_list = group_info['memVerList']
                cleaned_list = [item.replace('_0', '') for item in mem_ver_list]
                for user_id in cleaned_list:
                    mentions.append(Mention(user_id, offset=0, length=3000, auto_format=False))
                    time.sleep(0.00001)
                cc = MultiMention(mentions)
                self.send(Message(text=str(text_all), mention=cc), thread_id, thread_type)   
            except Exception as e:
                logging.error(f"Lỗi trong AllV3: {e}")      
        elif message.startswith("Call"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            try:
                parts = message.split()
                if len(parts) < 3:
                    self.replyMessage(
                        Message(text="ᴜꜱᴇ ᴄᴀʟʟ ᴜɪᴅ1 ᴜɪᴅ2 ᴜɪᴅ3 ... ᴄᴏᴜɴᴛ"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return
                target_ids = parts[1:-1]
                call_count = int(parts[-1])
                self.replyMessage(Message(text=f'''
┌─────────────────>
├>•ʙᴏᴛ ꜱᴘᴀᴍ ᴄᴀʟʟ ᴠɪᴘ
├•ꜱᴘᴀᴍ ᴄᴀʟʟ ꜱᴇɴᴛ ᴛᴏ:
├•ᴜꜱᴇʀ ɪᴅ: {', '.join(target_ids)}
├•ᴄᴀʟʟ: {call_count} ᴛɪᴍᴇꜱ
├>•ᴅᴜᴏɴɢ ɴɢᴏᴄ ʏᴇᴜ ǫᴜʏ̀ɴʜ ᴀɴʜ      
└─────────────────>'''), message_object, thread_id=thread_id, thread_type=thread_type)
                for target_id in target_ids:
                    threading.Thread(target=self.StartCall, args=(target_id, call_count), daemon=True).start()
            except Exception as e:
                print(f"Lỗi: {e}")
        elif message.startswith("ReoSp"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return

            if self.reo_spamming:
                  self.replyMessage(Message(text='𝙎𝙪𝙘𝙘𝙚𝙨𝙨 𝙁𝙪𝙡𝙡𝙮 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return

            mentions = message_object.mentions
            if not mentions:
                  self.replyMessage(Message(text='🚫 𝙐𝙨𝙚 𝙍𝙚𝙤 @𝙐𝙨𝙚𝙧.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return

            mentioned_user_id = mentions[0]['uid']

            self.reo_spamming = True
            self.reo_spam_thread = threading.Thread(target=self.reo_spam_message, args=(mentioned_user_id, thread_id, thread_type))
            self.reo_spam_thread.start()  
        elif message.startswith("StopR"):
          with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
          if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
          if not self.reo_spamming:
                  self.replyMessage(Message(text='🚫 𝙉𝙤𝙩 𝙎𝙥𝙖𝙢 𝙍𝙚𝙤 𝙍𝙪𝙣𝙣𝙞𝙣𝙜'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return
          self.reo_spamming = False
          if self.reo_spam_thread is not None:
            self.reo_spam_thread.join()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Info"):
            user_id = None
            if message_object.mentions:
                user_id = message_object.mentions[0]['uid']
            elif content[5:].strip().isnumeric():
                user_id = content[5:].strip()
            else:
                user_id = author_id
            user_info = self.fetchUserInfo(user_id)
            infozalo = self.checkinfo(user_id, user_info, thread_id)
            self.replyMessage(Message(text=infozalo, parse_mode="HTML"), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Spamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            args = message.strip().split()
            if len(args) == 1:
                self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙊𝙣 𝘿𝙚𝙡𝙖𝙮\n𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙊𝙛𝙛\n\n𝑽𝒅: 𝑺𝒑𝒂𝒎𝒗𝒊𝒑 𝑶𝒏 𝟓'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            if args[1].lower() == "off":
                self.dungspamvip()
                self.replyMessage(Message(text='✅ 𝙎𝙩𝙤𝙥 𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            if args[1].lower() == "on":
                if len(args) < 3 or not args[2].isdigit():
                    self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙊𝙣 𝘿𝙚𝙡𝙖𝙮\n\n𝑽𝒅: 𝑺𝒑𝒂𝒎𝒗𝒊𝒑 𝑶𝒏 𝟓'), 
                                      message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                    return
                try:
                    delay = float(args[2].strip())
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 𝙃𝙤𝙬 𝙏𝙤 𝘿𝙚𝙡𝙖𝙮 ?'), 
                                          message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                        return
                    self.chayspamvip_from_file(delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 𝙋𝙡𝙚𝙖𝙨𝙚 𝙄𝙣𝙥𝙪𝙩 𝘿𝙚𝙡𝙖𝙮'), 
                                      message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.replyMessage(Message(text='🚫 𝙄𝙣𝙘𝙤𝙧𝙧𝙚𝙘𝙩 𝙐𝙨𝙖𝙜𝙚 !\n𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙊𝙣 𝘿𝙚𝙡𝙖𝙮\n𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙊𝙛𝙛\n\n𝑽𝒅: 𝑺𝒑𝒂𝒎𝒗𝒊𝒑 𝑶𝒏 𝟓'), 
                              message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.lower().startswith("connect"):
            try:
                result = subprocess.run(["ping", "-c", "1", "google.com"], capture_output=True, text=True)
                for line in result.stdout.split("\n"):
                    if "time=" in line:
                        ping_time = line.split("time=")[-1].split(" ")[0]
                        self.replyMessage(Message(text=f'''
┌─────────────────>
├>•ᴛᴇꜱᴛ ᴘɪɴɢ ᴡɪꜰɪ ᴏʀ 𝟦ɢ
├•📶 ʏᴏᴜʀ ᴘɪɴɢ: {ping_time} ᴍꜱ
├•ʙᴏᴛ ᴢᴀʟᴏ ᴄᴏᴅᴇ ᴏꜰ ᴅᴜᴏɴɢ ɴɢᴏᴄ
├>•ᴅᴜᴏɴɢ ɴɢᴏᴄ ʏᴇᴜ ǫᴜʏ́ᴛ - ᴛᴍɪᴇᴇ
└─────────────────>'''), message_object, thread_id=thread_id, thread_type=thread_type)
                        return
                self.replyMessage(Message(text='''
┌─────────────────>
├>•ᴛᴇꜱᴛ ᴘɪɴɢ ᴡɪꜰɪ ᴏʀ 𝟦ɢ
├•📶 ʏᴏᴜʀ ᴘɪɴɢ: ʏᴏᴜʀ ᴡɪꜰɪ ᴏʀ 𝟦ɢ ᴅɪꜱᴄᴏɴɴᴇᴄᴛ ᴏʀ ʙᴏᴛ ʙᴜɢ ⚠️
├•ʙᴏᴛ ᴢᴀʟᴏ ᴄᴏᴅᴇ ᴏꜰ ᴅᴜᴏɴɢ ɴɢᴏᴄ
├>•ᴅᴜᴏɴɢ ɴɢᴏᴄ ʏᴇᴜ ǫᴜʏ́ᴛ - ᴛᴍɪᴇᴇ
└─────────────────>'''), message_object, thread_id=thread_id, thread_type=thread_type) 
            except Exception as e:
                self.replyMessage(Message(text='⚠️ ᴅɪꜱᴄᴏɴɴᴇᴄᴛ!'), 
                                  message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Spam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 𝙃𝙤𝙬 𝙏𝙤 𝘿𝙚𝙡𝙖𝙮 ?'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                        return
                    self.chayspam(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 𝙋𝙡𝙚𝙖𝙨𝙚 𝙄𝙣𝙥𝙪𝙩 𝘿𝙚𝙡𝙖𝙮'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            else:
                self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙎𝙥𝙖𝙢 𝙏𝙚𝙭𝙩 𝘿𝙚𝙡𝙖𝙮\n\n𝑺𝒑𝒂𝒎 𝑵𝒈𝒐𝒄 𝟓'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("StopSpam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.dungspam()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙥𝙖𝙢 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Off"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.replyMessage(Message(text='𝙊𝙛𝙛 ! - 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 𝙁𝙪𝙡𝙡'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            exit()
        elif message.startswith("All"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(
                Message(text='🚫 ᴏɴʟʏ ᴅᴜᴏɴɢ ɴɢᴏᴄ 🥀 ᴄᴀɴ ʙᴇ ᴜꜱᴇ.'),
                message_object, thread_id=thread_id, thread_type=thread_type,
                ttl=30000
                )
                return
            message_content = message[4:].strip() 
            if not message_content:
                self.replyMessage(
                    Message(text="🚫 𝑷𝒍𝒆𝒂𝒔𝒆 𝑰𝒏𝒑𝒖𝒕 𝑻𝒆𝒙𝒕 𝑭𝒐𝒓 𝑨𝒍𝒍 !"),
                    message_object, thread_id=thread_id, thread_type=thread_type,
                    ttl=30000
                )
                return
            mention = Mention("-1", length=len(message_content) + 1, offset=1)
            message_obj = Message(text=message_content, mention=mention)
            self.send(message_obj, thread_id=thread_id, thread_type=thread_type)
    def QuynhAnhXinh(self, thread_id, user_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']
        return user_id in admin_ids or user_id == creator_id
    def spam_message(self, spam_content, thread_id, thread_type):
        """Spam the content from content.txt file in the thread."""
        words = spam_content.split()
        while self.spamming:
            for word in words:
                if not self.spamming:
                    break
                mention = Mention(uid='-1', offset=0, length=len(word))
                spam_message = Message(text=word, mention=mention)
                self.send(spam_message, thread_id=thread_id, thread_type=thread_type)
                time.sleep(0.5)

    def reo_spam_message(self, mentioned_user_id, thread_id, thread_type):
        """Spam mentions of a specific user."""
        while self.reo_spamming:
            mention = Mention(uid=mentioned_user_id, offset=0, length=5)
            spam_message = Message(text="@user", mention=mention)
            self.send(spam_message, thread_id=thread_id, thread_type=thread_type, ttl=1000)
            time.sleep(0)
    def chayspamvip_from_file(self, delay, thread_id, thread_type):
        if self.spammingvip:
            self.dungspamvip()
        self.spammingvip = True
        self.spam_threadvip = threading.Thread(target=self.spamtagallvip_from_file, args=(delay, thread_id, thread_type))
        self.spam_threadvip.start()
    def dungspamvip(self):
        if self.spammingvip:
            self.spammingvip = False
            if self.spam_threadvip is not None:
                self.spam_threadvip.join()
            self.spam_threadvip = None
    def spamtagallvip_from_file(self, delay, thread_id, thread_type):
        try:
            with open("Quyt.txt", "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
            if not lines:
                logging.error("⚠️ War.txt is empty or not found!")
                return
        except FileNotFoundError:
            logging.error("❌ War.txt not found!")
            return
        while self.spammingvip:
            try:
                message = random.choice(lines)
                mention = Mention("-1", length=len(message) + 1, offset=1)
                message_obj = Message(text=message, mention=mention)
                self.send(message_obj, thread_id=thread_id, thread_type=thread_type, ttl=10000)
                time.sleep(delay)
            except Exception as e:
                logging.error(f"❌ Error during spamtagallvip_from_file: {e}")
                break
    def chayspam(self, message, delay, thread_id, thread_type):
        if self.spamming:
            self.dungspam()
        self.spamming = True
        self.spam_thread = threading.Thread(target=self.spamtagall, args=(message, delay, thread_id, thread_type))
        self.spam_thread.start()
    def dungspam(self):
        if self.spamming:
            self.spamming = False
            if self.spam_thread is not None:
                self.spam_thread.join()
            self.spam_thread = None
    def spamtagall(self, message, delay, thread_id, thread_type):
        while self.spamming:
            try:
                logging.debug(f"Sending message: {message}, thread_id: {thread_id}, thread_type: {thread_type}")
                message_obj = Message(text=message)
                self.send(message_obj, thread_id=thread_id, thread_type=thread_type, ttl=10000)
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error during spamtagall: {e}")
                break
    def checkinfo(self, user_id, user_info, thread_id):
        if 'changed_profiles' in user_info and user_id in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][user_id]
            infozalo = f'''
> ┌─────────────────────
> ├> <b>ɴᴀᴍᴇ: </b> {profile.get('displayName', '')}
> ├> <b>ɪᴅ-ᴜꜱᴇʀ: </b> {profile.get('userId', '')}
> ├> <b>ɪᴅ-ɢʀᴏᴜᴘ: </b> {thread_id}
> └─────────────────────
        '''
            return infozalo
        else:
            return "Thông tin không tồn tại."
    
client = QuynhAnh(
    '</>', '</>',
    imei="1469a7a7-640c-45c9-a106-6d02fd8859ed-50041963ae561cfabe9225edff35b18f",
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    session_cookies={"_gid":"GA1.2.877494567.1743050845","zputm_source":"","zputm_medium":"","zputm_campaign":"","zpsrc":"","_ga_1J0YGQPT22":"GS1.1.1743050890.1.1.1743050904.46.0.0","_ga":"GA1.2.1699182513.1743050845","_ga_VM4ZJE1265":"GS1.2.1743050846.1.1.1743051004.0.0.0","_ga_RYD7END4JE":"GS1.2.1743051079.1.1.1743051097.42.0.0","_zlang":"vn","__zi":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8yvaUgdcazOZtAPwgVLJbgAS9dleZCs.1","__zi-legacy":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8yvaUgdcazOZtAPwgVLJbgAS9dleZCs.1","ozi":"2000.QOBlzDCV2uGerkFzm09GrstLxFFF2rhP9zteyO0AMDmbtUtqCpO.1","app.event.zalo.me":"8828299983234192141","zpsid":"2brN.378747974.1._pc9llLKg1wpQ3i8-LIe7e0dsYt2R9ygmcsVAjyWtDPAMX2pz7Ju-v9Kg1u","zpw_sek":"67fX.378747974.a0.9n4ukDU4YjAHk1d4zeIAqgocxxdrlgYOiUFQclpkuPsmo_hXWUtFu_ZBnAYmkRVmggx-fXyxX6fwXQk2CkEAqW"})
client.listen()