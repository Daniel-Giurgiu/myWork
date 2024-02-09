import unittest
from custom_framework import CustomWebFramework

class TestFramework(unittest.TestCase):
    def __init__(self):
        self.custom_framework = CustomWebFramework()
    
    def test_check_simple_path(self):
        server_path = "/add"
        client_path = "/add"
        
        res = self.custom_framework.check_simple_path(server_path.split("/"), client_path.split("/"))
        self.assertEqual(res, True)
        
        server_path = "/add"
        client_path = "/add/"
        
        res = self.custom_framework.check_simple_path(server_path.split("/"), client_path.split("/"))
        self.assertEqual(res, True)
        
        server_path = "/add/<id>"
        client_path = "/add/5"
        
        res = self.custom_framework.check_simple_path(server_path.split("/"), client_path.split("/"))
        self.assertEqual(res, True)
        