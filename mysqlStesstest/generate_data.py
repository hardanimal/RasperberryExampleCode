# encoding: utf-8

__author__ = 'Danzel.Li'

import os, base64, random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import time

import pymysql


@dataclass
class RecordsEntry:
    record_id: int = None
    hostname : str = None
    encrypt_key : str = None
    used : int = None

class RecordsDb(ABC):
    @abstractmethod
    def insert(
        self,
        table_name: str,
        hostname: str,
        encrypt_key: str,
        used: int,
    ) -> bool:
        """
        Insert one record
        """
        pass

class MysqlStressTestDb(RecordsDb):
    def __init__(self, connection_config: Dict):
        self.connection_config = connection_config
        self.connection_config["cursorclass"] = pymysql.cursors.DictCursor

    def insert(self, table_name: str, hostname: str, encrypt_key: str, used: int) -> bool:
        connection = pymysql.connect(**self.connection_config)
        count_query = f"INSERT INTO {table_name} (hostname, encrypt_key, used) VALUES (%s, %s, %s)"
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(count_query, (hostname, encrypt_key, used))
            connection.commit()
        return True

class GenerateKey:
    
    def __init__(self):
        self.instance = {}
        try:
            import socket
            self.instance["hostname"] = socket.gethostname()
        except:
            self.instance["hostname"] = "WORKSTATION"
        
    def NewKey(self) -> Dict:
        random_bytes = os.urandom(256)
        self.instance["encrypt_key"] = base64.b64encode(random_bytes).decode('utf-8')
        self.instance["used"] = random.randint(0,1)
        return self.instance


if __name__ == "__main__":
    setrecord = MysqlStressTestDb({"host": "192.168.0.201", "user": "test", "password": "s20jjut4Xd8=", "database": "stresstest"})
    KeyData = GenerateKey()
    print("start test")

    time_start = time.time()
    for i in range(1000000):
        OneKey = KeyData.NewKey()
        print(OneKey)
        setrecord.insert("keys_1", OneKey["hostname"], OneKey["encrypt_key"], OneKey["used"])

    time_end = time.time() #记录计算结束时间
    print(f'计算共用时{time_end - time_start}秒')
