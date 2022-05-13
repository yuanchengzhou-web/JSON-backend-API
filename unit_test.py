import requests

base = "http://127.0.0.1:5000/"

class unittest:

    def __init__(self, base):
        self.base = base
    
    def test_ping(self):
        response = requests.get(self.base+"api/ping")
        try:
            assert response.status_code == 200
            print(response.json())
        except AssertionError:
            print(response.json())

    def test_posts(self, inputs: dict):
        response = requests.get(self.base+"/api/posts", json=inputs)
        try:
            assert response.status_code == 200
            print(response.json())
        except AssertionError:
            print(response.json())

# The test cases
inputs1 = {"tags":"", "sortBy":None, "direction":None}
inputs2 = {"tags":"tech, love, history", "sortBy":None, "direction":None}
inputs3 = {"tags":"tech, love, history", "sortBy":"likes", "direction":"desc"}
inputs4 = {"tags":"tech, love, history", "sortBy":"food", "direction":"desc"}
inputs5 = {"tags":"tech, love, history", "sortBy":"likes", "direction":"flat"}
all_inputs = [inputs1, inputs2, inputs3, inputs4, inputs5]
test = unittest(base)
test.test_ping()
for i in all_inputs:
    print("---------------------------------------------------------")
    print(" ")
    test.test_posts(i)
    