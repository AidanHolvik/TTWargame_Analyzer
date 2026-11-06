from flaskr import create_app

# test whether the app config matches the TESTING setting
def test_configMatchesTestingMode():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing

