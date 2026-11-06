import pytest
from flaskr.db import get_db

class TestIndex:
    def test_get (client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Breacher Team" in response.data

class TestCreate:
    def test_get(client):
        response = client.get("/create")
        assert response.status_code == 200
        assert b"New Unit" in response.data

    def test_post_goodInputs(client):
        response = client.post("/create", data={"name": "New Unit"})
        assert response.status_code == 303  # Assuming a redirect after successful creation

    # TODO: test_post_badName
    # TODO: test_post_duplicateName

class TestModify:
    # TODO: make dependent on get_unit and get_unit_models_for_inputs
    def test_get_existingNoModels(client):
        response = client.get("/modify/1")
        assert response.status_code == 200
        assert b"Modify Unit" in response.data
        # TODO: ensure get_unit is called with the correct ID
        # TODO: ensure the existing unit's details are correctly displayed

    # TODO: make dependent on get_unit and get_unit_models_for_inputs
    def test_get_existingWithModels(client):
        pass
    
    def test_get_nonExisting(client):
        response = client.get("/modify/999")
        assert response.status_code == 404

    # TODO: test_post_noModelsGoodInputs
    # TODO: test_post_goodInputs
    # TODO: test_post_badInput (parameterized)
    # TODO: test_post_duplicateName
    # TODO: test_post_missingField
    # TODO: test_post_badQuantity
    # TODO: test_post_missingQuantity?

class TestDelete:
    pass
    # TODO: test_delete_existing_withoutModels
    # TODO: test_delete_existing_withModels
    # TODO: test_delete_existing_withModelsAndDependencies?
    # TODO: test_delete_existing_identicalUnit
        # Should test scenario where identical unit exists. Make sure deletion only affects the intended unit.
    # TODO: test_delete_nonExisting

    # TODO: test_delete_withModels

# TODO: test function get_unit_models_for_inputs from unit.py
    # TODO: test_get_unit_models_for_inputs
    # TODO: test_get_unit_models_for_inputs_noModels
    # TODO: test_get_unit_models_for_inputs_badId

